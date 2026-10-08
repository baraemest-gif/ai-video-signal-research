package com.alarm.premium

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

object AlarmStore {
    private const val PREFS = "alarm_prefs"
    private const val KEY = "alarms"

    fun load(context: Context): MutableList<AlarmModel> {
        val raw = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getString(KEY, "[]") ?: "[]"
        val out = mutableListOf<AlarmModel>()
        runCatching {
            val a = JSONArray(raw)
            for (i in 0 until a.length()) {
                val o = a.getJSONObject(i)
                val daysArray = o.optJSONArray("days") ?: JSONArray()
                val days = mutableSetOf<Int>()
                for (j in 0 until daysArray.length()) days += daysArray.getInt(j)
                out += AlarmModel(
                    id = o.getInt("id"),
                    hour = o.getInt("hour"),
                    minute = o.getInt("minute"),
                    label = o.optString("label", "المنبّه"),
                    days = days,
                    enabled = o.optBoolean("enabled", true)
                )
            }
        }
        return out
    }

    fun save(context: Context, alarms: List<AlarmModel>) {
        val a = JSONArray()
        alarms.forEach { alarm ->
            val days = JSONArray()
            alarm.days.sorted().forEach { days.put(it) }
            a.put(JSONObject().apply {
                put("id", alarm.id)
                put("hour", alarm.hour)
                put("minute", alarm.minute)
                put("label", alarm.label)
                put("days", days)
                put("enabled", alarm.enabled)
            })
        }
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putString(KEY, a.toString()).apply()
    }

    fun updateEnabled(context: Context, id: Int, enabled: Boolean) {
        val all = load(context)
        val index = all.indexOfFirst { it.id == id }
        if (index >= 0) {
            all[index] = all[index].copy(enabled = enabled)
            save(context, all)
        }
    }

    fun get(context: Context, id: Int): AlarmModel? = load(context).firstOrNull { it.id == id }
}
