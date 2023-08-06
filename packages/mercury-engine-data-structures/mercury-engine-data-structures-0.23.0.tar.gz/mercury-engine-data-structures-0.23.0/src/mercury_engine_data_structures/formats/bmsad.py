import construct
from construct.core import (
    Array,
    Byte,
    Const,
    Construct,
    Flag,
    Float32l,
    Hex,
    IfThenElse,
    Int8ul,
    Int16ul,
    Int32ul,
    PrefixedArray,
    Struct,
    Switch,
)

from mercury_engine_data_structures import common_types, game_check, type_lib
from mercury_engine_data_structures.common_types import Char, Float, StrId, make_dict, make_vector
from mercury_engine_data_structures.construct_extensions.alignment import PrefixedAllowZeroLen
from mercury_engine_data_structures.construct_extensions.misc import ErrorWithMessage
from mercury_engine_data_structures.formats import BaseResource, dread_types
from mercury_engine_data_structures.formats.property_enum import PropertyEnum
from mercury_engine_data_structures.game_check import Game


def SR_or_Dread(sr, dread):
    return IfThenElse(
        game_check.current_game_at_most(Game.SAMUS_RETURNS),
        sr,
        dread,
    )


FunctionArgument = Struct(
    type=Char,
    value=Switch(
        construct.this.type,
        {
            's': StrId,
            'f': Float,
            'b': Flag,
            'i': Int32ul,
        },
        ErrorWithMessage(lambda ctx: f"Unknown argument type: {ctx.type}", construct.SwitchError)
    )
)
Functions = make_vector(Struct(
    name=StrId,
    unk=Int16ul,
    params=common_types.DictAdapter(common_types.make_vector(
        common_types.DictElement(
            FunctionArgument,
            key=PropertyEnum,
        )
    )),
))

fieldtypes = {k: v for k, v in vars(dread_types).items() if isinstance(v, construct.Construct)}


def find_charclass_for_type(type_name: str):
    if type_name == "CActorComponent":
        return "CActorComponentDef"

    as_char = "CCharClass" + type_name[1:]
    if as_char in fieldtypes:
        return as_char

    return find_charclass_for_type(
        type_lib.get_parent_for(type_name),
    )


def DreadDependencies():
    component_dependencies = {
        "CFXComponent": make_vector(Struct(
            "file" / StrId,
            "unk1" / Int32ul,
            "unk2" / Int32ul,
            "unk3" / Byte
        )),
        "CCollisionComponent": Struct(
            "file" / StrId,
            "unk" / Int16ul
        ),
        "CGrabComponent": make_vector(Struct(
            "unk1" / StrId,
            "unk2" / StrId,
            "unk3" / StrId,
            "unk4" / Float32l,
            "unk5" / Byte,
            "unk6" / Byte,
            "unk7" / Int16ul,
            "unk8" / Array(2, Struct(
                "unk2" / Int16ul,
                "unk1" / Array(8, Float32l),
            )),
        )),
        "CBillboardComponent": Struct(
            "id1" / StrId,
            "unk1" / make_vector(Struct(
                "id" / StrId,
                "unk1" / Array(3, Int32ul),
                "unk2" / Byte,
                "unk3" / Array(2, Int32ul),
                "unk4" / Float32l
            )),
            "id2" / StrId,
            "unk2" / make_vector(Struct(
                "id" / StrId,
                "unk1" / Byte,
                "unk2" / Array(4, Int32ul)
            )),
        ),
        "CSwarmControllerComponent": Struct(
            "unk1" / make_vector(StrId),
            "unk2" / make_vector(StrId),
            "unk3" / make_vector(StrId)
        )
    }
    component_dependencies["CStandaloneFXComponent"] = component_dependencies["CFXComponent"]

    def component_type(this):
        for component_type in component_dependencies.keys():
            if type_lib.is_child_of(this.type, component_type):
                return component_type
        return None

    return Switch(component_type, component_dependencies)


ExtraFields = common_types.DictAdapter(common_types.make_vector(
    common_types.DictElement(Struct(
        "type" / StrId,
        "value" / Switch(
            construct.this.type,
            {
                "bool": Flag,
                "string": StrId,
                "float": Float,

                "int": construct.Int32sl,
                "vec3": Float[3],
            },
            ErrorWithMessage(lambda ctx: f"Unknown argument type: {ctx.type}", construct.SwitchError)
        )
    ))
), allow_duplicates=True)

DreadComponent = Struct(
    type=StrId,
    unk_1=Array(2, Hex(Int32ul)),
    fields=PrefixedAllowZeroLen(
        Int32ul,
        Struct(
            empty_string=PropertyEnum,
            root=PropertyEnum,
            fields=Switch(
                lambda ctx: find_charclass_for_type(ctx._._.type),
                fieldtypes,
                ErrorWithMessage(lambda ctx: f"Unknown component type: {ctx._._.type}", construct.SwitchError)
            )
        )
    ),
    extra_fields=construct.If(
        lambda this: type_lib.is_child_of(this.type, "CComponent"),
        ExtraFields,
    ),
    functions=Functions,
    dependencies=DreadDependencies(),
)

CCharClass = Struct(
    model_name=StrId,
    unk_1=Int16ul,
    unk_2=Int32ul,
    unk_3=Int16ul,
    sub_actors=PrefixedArray(Int32ul, StrId),
    unk_4=Array(9, Float32l),
    magic=Const(0xFFFFFFFF, Hex(Int32ul)),
    unk_5=Byte,
    unk_6=StrId,
    unk_7=Byte,

    components=make_dict(DreadComponent),

    binaries=make_vector(StrId),
    sources=make_vector(StrId >> Byte),
)

CActorDef = Struct(
    unk_1=Int16ul,
    unk_2=Int32ul,
    unk_3=Int16ul,
    sub_actors=PrefixedArray(Int32ul, StrId),
    unk_4=StrId,

    components=make_dict(DreadComponent),

    binaries=make_vector(StrId),
    sources=make_vector(StrId >> Byte),
)

property_types = {
    "CCharClass": CCharClass,
    "CActorDef": CActorDef
}


#


def SRDependencies():
    component_dependencies = {
        "CAnimationComponent": make_vector(StrId),
        "CFXComponent": make_vector(Struct(
            "file" / StrId,
            "unk1" / Int32ul,
            "unk2" / Int32ul,
        )),
        "CCollisionComponent": Struct(
            "file" / StrId,
            "unk" / Int16ul
        ),
        "CGrabComponent": make_vector(Struct(
            a=StrId,
            b=StrId,
            c=StrId,
            d=Hex(Int32ul)[2],
            e=Float[8],
            f=Hex(Int32ul)[9],
        )),
        "CGlowflyAnimationComponent": make_vector(StrId),
        "CSceneModelAnimationComponent": make_dict(make_dict(StrId)),

        "CBillboardComponent": Struct(
            "id1" / StrId,
            "unk1" / make_dict(Struct(
                "unk1" / Int32ul[3],
                "unk2" / Byte,
                "unk3" / Int32ul[2],
                "unk4" / Float32l
            )),
            "id2" / StrId,
            "unk3" / make_vector(Struct(
                "id" / StrId,
                "unk1" / Byte,
                "unk2" / make_vector(Struct(
                    "a" / Float,
                    "b" / Float,
                    "c" / Float,
                )),
            )),
        ),

        "CSwarmControllerComponent": Struct(
            "unk1" / make_vector(StrId),
            "unk2" / make_vector(StrId),
            "unk3" / make_vector(StrId)
        ),
    }
    for dep in [
        "CTsumuriAcidDroolCollision",
        "CBillboardCollisionComponent",
        "CQueenPlasmaArcCollision",
    ]:
        component_dependencies[dep] = component_dependencies["CCollisionComponent"]

    for dep in [
        "CFlockingSwarmControllerComponent",
        "CBeeSwarmControllerComponent",
    ]:
        component_dependencies[dep] = component_dependencies["CSwarmControllerComponent"]

    return Switch(construct.this.type, component_dependencies)


SR_Component = Struct(
    type=StrId,
    unk_1=Hex(Int32ul)[2],
    functions=Functions,

    extra_fields=ExtraFields,
    dependencies=SRDependencies(),
)

BMSAD_SR = Struct(
    _magic=Const(b"MSAD"),
    version=Const(0x002C0001, Hex(Int32ul)),

    name=StrId,
    model_name=StrId,

    unk_1=Int8ul,
    unk_2=Float[9],
    unk_3=Int8ul,
    unk_4=Int32ul,
    other_magic=Const(0xFFFFFFFF, Hex(Int32ul)),
    unk_5=Int16ul,
    unk_6=StrId[2],
    unk_7=Int8ul,
    sub_actors=make_vector(StrId),
    unk_8=Int32ul,

    # count=Int32ul,
    # component=(StrId >> SR_Component)[4],
    components=make_dict(SR_Component),

    binaries=make_vector(StrId),

    rest=construct.GreedyBytes,
    _end=construct.Terminated,
)

BMSAD_Dread = Struct(
    _magic=Const(b"MSAD"),
    version=Const(0x0200000F, Hex(Int32ul)),

    # # gameeditor::CGameModelRoot
    # root_type=construct.Const('Root', PropertyEnum),
    # Root=gameeditor_CGameModelRoot,

    name=StrId,
    type=StrId,

    property=Switch(
        construct.this.type,
        property_types,
        ErrorWithMessage(lambda ctx: f"Unknown property type: {ctx.type}"),
    ),
    _end=construct.Terminated,
)


class Bmsad(BaseResource):
    @classmethod
    def construct_class(cls, target_game: Game) -> Construct:
        return {
            Game.SAMUS_RETURNS: BMSAD_SR,
            Game.DREAD: BMSAD_Dread,
        }[target_game]
