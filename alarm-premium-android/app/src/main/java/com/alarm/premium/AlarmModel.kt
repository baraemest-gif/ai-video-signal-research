package com.alarm.premium

data class AlarmModel(
    val id: Int,
    val hour: Int,
    val minute: Int,
    val label: String,
    val days: Set<Int>,
    val enabled: Boolean
)
