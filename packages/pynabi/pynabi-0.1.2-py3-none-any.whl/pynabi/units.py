from typing import Union as _Un, Optional as _Op, Tuple as _Tu, Self as  _Self, Any as _Any
from ._common import Vec3D as _V

class _AbMeasure:
    _U: _Tu[_Tu[float, str],...] = ()
    _R = (1.0, 0)

    def __init__(self, value: float, unit: int) -> None:
        """Do not use this constructor"""
        self._v = value
        self._u = unit

    def __mul__(self, other: _Un[int,float]) -> _Self:
        if type(other) is int or type(other) is float:
            return type(self)(self._v*other, self._u) # type: ignore
        else:
            return NotImplemented

    def __rmul__(self, other: _Un[int,float]) -> _Self:
        return type(self).__mul__(self, other)

    def __add__(self, other: _Self):
        if type(other) is not Length:
            return NotImplemented
        U = type(self)._U
        delta = other._v * U[other._u][0] / U[self._u][0]
        return type(self)(self._v + delta, self._u);

    def __sub__(self, other: _Self) -> '_Self':
        if type(other) is not Length:
            return NotImplemented # type: ignore
        U = type(self)._U
        delta = other._v * U[other._u][0] / U[self._u][0]
        return type(self)(self._v - delta, self._u);

    def __neg__(self):
        return type(self)(-self._v, self._u)

    def __str__(self):
        return f"{self._v} {type(self)._U[self._u][1]}"
    
    def setAsReference(self):
        type(self)._R = (self._v, self._u)
    
    @classmethod
    def fromReference(cls, value: float, ref: _Op[_Self]) -> _Self:
        assert type(value) is float or type(value) is int, f"Value of {cls.__name__} must be a number"
        if ref is None:
            return cls(value*cls._R[0], cls._R[1])
        else:
            assert type(ref) is cls, f"Reference for a {cls.__name__} mus be a {cls.__name__} itself"
            return value*ref

    @classmethod
    def sanitize(cls, value: _Any) -> _Self:
        t = type(value)
        if t is float or t is int:
            return cls(value*cls._R[0], cls._R[1])
        elif t is cls:
            return value
        else:
            raise TypeError(f"Cannot construct {cls.__name__} from {value} (of type {t})")
        
    @classmethod
    def getDefaultReference(cls):
        return cls(cls._R[0], cls._R[1])


class Length(_AbMeasure):
    _U = ((0.529177249, "Bohr"), (1.0, "Angstrom"), (10.0, "nm"))


Bohr = Length(1.0, 0)
Ang = Length(1.0, 1)
nm = Length(1.0, 2)


class Energy(_AbMeasure):
    _U = (
        (27.2114, "Ha"),
        (1.0, "eV"),
        (13.6057039763, "Ry"),
        (8.617328149741e-5, "K")
    )


Ha = Energy(1.0, 0)
eV = Energy(1.0, 1)
Ry = Energy(1.0, 2)
Kelvin = Energy(1.0, 3)


class Pos3D:
    def __init__(self, x: float, y: float, z: float, unit: _Op[Length] = None) -> None:
        m = 1.0
        if unit is None:
            m = Length._R[0]
            self.u = Length._R[1]
        elif type(unit) is Length:
            m = unit._v
            self.u = unit._u
        else:
            raise TypeError("3D Position reference must be a Length itself")
        self.x = x*m
        self.y = y*m
        self.z = z*m
    
    def __str__(self) -> str:
        return f"{self.x} {self.y} {self.z} {Length._U[self.u][1]}"
    
    @staticmethod
    def uniform(l: _Un[float,'Length']):
        return Pos3D(1,1,1,Length.sanitize(l))
    
    @staticmethod
    def sanitize(v: _Any) -> 'Pos3D':
        t = type(v)
        if t is Pos3D:
            return v
        elif t is _V:
            return Pos3D(v.x,v.y,v.z)
        else:
            raise TypeError(f"Cannot construct Pos3D from {v} (of type {t})")