#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import datetime


class Money:
    def __init__(
        self,
        currency: str,
        when: datetime,
        integral: int,
        mantissa: int,
    ) -> None:
        self.currency = currency
        self.when = when
        self.integral = integral
        self.mantissa = mantissa

    def __repr__(self) -> str:
        return f"{self.currency} {self.integral}.{self.mantissa} on {self.when.strftime('%Y %b %d')}"

    def __neg__(self):
        return Money(
            currency=self.currency,
            when=self.when,
            integral=-self.integral,
            mantissa=self.mantissa,
        )

    def __add__(self, other):
        if isinstance(other, (float, int)):
            mantissa = other - int(other)
            total_mantissa = self.mantissa + int(mantissa)
            return Money(
                currency=self.currency,
                when=self.when,
                integral=self.integral + int(other) + total_mantissa // 100,
                mantissa=total_mantissa % 100,
            )
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise NotImplementedError(
                    "Attempting to add monies of different currencies."
                )
            if self.when != other.when:
                raise NotImplementedError(
                    "Attempting to add monies from different datetimes. Adjust for inflation."
                )

            total_mantissa = self.mantissa + other.mantissa

            return Money(
                currency=self.currency,
                when=self.when,
                integral=self.integral + other.integral + total_mantissa // 100,
                mantissa=total_mantissa % 100,
            )

        raise NotImplementedError(f"Addition not implemented for type: {type(other)}")

    def __sub__(self, other):
        if isinstance(other, (float, int)):
            mantissa = other - int(other)
            total_mantissa = self.mantissa - int(mantissa)
            return Money(
                currency=self.currency,
                when=self.when,
                integral=self.integral - int(other) + total_mantissa // 100,
                mantissa=total_mantissa % 100,
            )
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise NotImplementedError(
                    "Attempting to add monies of different currencies."
                )
            if self.when != other.when:
                raise NotImplementedError(
                    "Attempting to add monies from different datetimes. Adjust for inflation."
                )

            total_mantissa = self.mantissa + other.mantissa

            return Money(
                currency=self.currency,
                when=self.when,
                integral=self.integral - other.integral + total_mantissa // 100,
                mantissa=total_mantissa % 100,
            )

        raise NotImplementedError(f"Addition not implemented for type: {type(other)}")

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            total_cents = (100 * self.integral + self.mantissa) * other
            total_dollars, total_cents = divmod(total_cents, 100)
            return Money(
                currency=self.currency,
                when=self.when,
                integral=int(total_dollars),
                mantissa=round(total_cents),
            )

        raise NotImplementedError(
            f"Multiplication not implemented for type: {type(other)}"
        )

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            total_cents = (100 * self.integral + self.mantissa) / other
            total_dollars, total_cents = divmod(total_cents, 100)
            return Money(
                currency=self.currency,
                when=self.when,
                integral=int(total_dollars),
                mantissa=round(total_cents),
            )

        if isinstance(other, Money):
            if self.currency != other.currency:
                raise NotImplementedError(
                    "Attempting to divide monies of different currencies."
                )
            if self.when != other.when:
                raise NotImplementedError(
                    "Attempting to divide monies from different datetimes. Adjust for inflation."
                )

            total_cents = (100 * self.integral + self.mantissa) / (100 * other.integral + other.mantissa)
            return float(total_cents)

        raise NotImplementedError(
            f"Division not implemented for type: {type(other)}"
        )

    def __eq__(self, other) -> bool:
        if (
            self.currency == other.currency
            and self.integral == other.integral
            and self.mantissa == other.mantissa
            and self.when == other.when
        ):
            return True
        return False
