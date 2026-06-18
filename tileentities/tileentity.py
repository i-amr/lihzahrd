from __future__ import annotations
from ..fileutils import Coordinates
from .targetdummy import TargetDummy
from .itemframe import ItemFrame
from .logicsensor import LogicSensor
from .mannequin import Mannequin
from .weaponrack import WeaponRack
from .hatrack import HatRack
from .plate import Plate
from .pylon import Pylon
from .itemflask import ItemFlask
from .kiteanchor import KiteAnchor
from .critteranchor import CritterAnchor


class TileEntity:
	"""A TileEntity, such as a Training Dummy, an Item Frame or a Logic Sensor."""

	__slots__ = "id", "position", "extra"

	def __init__(
		self,
		id_: int,
		position: Coordinates,
		extra: TargetDummy | ItemFrame | LogicSensor,
	):
		self.id: int = id_
		self.position: Coordinates = position
		self.extra: TargetDummy | ItemFrame | LogicSensor = extra

	def __repr__(self):
		return f"<TileEntity {self.id} at {self.position} ({repr(self.extra)})>"

	@classmethod
	def read(cls, fr: FileReader, version: Version) -> TileEntity:
		te_type = fr.uint1()

		te_id = fr.int4()
		te_position = Coordinates(fr.int2(), fr.int2())
		te_extra = None

		match te_type:
			case 0 :  # TETrainingDummy.cs
				te_extra = TargetDummy.read(fr)
			case 1 :  # TEItemFrame.cs
				te_extra = ItemFrame.read(fr)
			case 2 :  # TELogicSensor.cs
				te_extra = LogicSensor.read(fr)
			case 3 :  # TEDisplayDoll.cs
				te_extra = Mannequin.read(fr, version)
			case 4 :  # TEWeaponsRack.cs
				te_extra = WeaponRack.read(fr)
			case 5 :  # TEHatRack.cs
				te_extra = HatRack.read(fr)
			case 6 :  # TEFoodPlatter.cs
				te_extra = Plate.read(fr)
			case 7 :  # TETeleportationPylon.cs
				te_extra = Pylon()
			case 8 :  # TEDeadCellsDisplayJar.cs
				te_extra = ItemFlask.read(fr)
			case 9 :  # TEKiteAnchor.cs
				te_extra = KiteAnchor.read(fr)
			case 10:  # TECritterAnchor.cs
				te_extra = CritterAnchor.read(fr)

		return cls(
			id_=te_id,
			position=te_position,
			extra=te_extra,
		)
