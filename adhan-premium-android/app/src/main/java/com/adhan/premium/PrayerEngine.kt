package com.adhan.premium

import com.batoulapps.adhan.CalculationMethod
import com.batoulapps.adhan.CalculationParameters
import com.batoulapps.adhan.Coordinates
import com.batoulapps.adhan.DateComponents
import com.batoulapps.adhan.Madhab
import com.batoulapps.adhan.PrayerTimes
import java.time.Instant
import java.time.LocalDate

object PrayerEngine {
    data class DayTimes(
        val date: LocalDate,
        val fajr: Instant,
        val sunrise: Instant,
        val dhuhr: Instant,
        val asr: Instant,
        val maghrib: Instant,
        val isha: Instant
    ) {
        fun all(): LinkedHashMap<String, Instant> = linkedMapOf(
            "الفجر · Fajr" to fajr,
            "الشروق · Sunrise" to sunrise,
            "الظهر · Dhuhr" to dhuhr,
            "العصر · Asr" to asr,
            "المغرب · Maghrib" to maghrib,
            "العشاء · Isha" to isha
        )

        fun adhanOnly(): LinkedHashMap<String, Instant> = linkedMapOf(
            "الفجر · Fajr" to fajr,
            "الظهر · Dhuhr" to dhuhr,
            "العصر · Asr" to asr,
            "المغرب · Maghrib" to maghrib,
            "العشاء · Isha" to isha
        )
    }

    fun calculate(
        latitude: Double,
        longitude: Double,
        date: LocalDate,
        methodName: String,
        hanafi: Boolean
    ): DayTimes {
        val coordinates = Coordinates(latitude, longitude)
        val components = DateComponents(date.year, date.monthValue, date.dayOfMonth)
        val params = parameters(methodName)
        params.madhab = if (hanafi) Madhab.HANAFI else Madhab.SHAFI
        val p = PrayerTimes(coordinates, components, params)
        return DayTimes(
            date, p.fajr.toInstant(), p.sunrise.toInstant(), p.dhuhr.toInstant(),
            p.asr.toInstant(), p.maghrib.toInstant(), p.isha.toInstant()
        )
    }

    fun parameters(name: String): CalculationParameters = when (name) {
        "Umm al-Qura" -> CalculationMethod.UMM_AL_QURA.parameters
        "Egyptian" -> CalculationMethod.EGYPTIAN.parameters
        "Karachi" -> CalculationMethod.KARACHI.parameters
        "North America" -> CalculationMethod.NORTH_AMERICA.parameters
        "Turkey" -> CalculationMethod.TURKEY.parameters
        "Dubai" -> CalculationMethod.DUBAI.parameters
        "Qatar" -> CalculationMethod.QATAR.parameters
        "Kuwait" -> CalculationMethod.KUWAIT.parameters
        "Singapore" -> CalculationMethod.SINGAPORE.parameters
        "Moon Sighting Committee" -> CalculationMethod.MOON_SIGHTING_COMMITTEE.parameters
        else -> CalculationMethod.MUSLIM_WORLD_LEAGUE.parameters
    }

    val methods = arrayOf(
        "Muslim World League","Umm al-Qura","Egyptian","Karachi","North America",
        "Turkey","Dubai","Qatar","Kuwait","Singapore","Moon Sighting Committee"
    )
}
