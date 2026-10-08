package com.adhan.premium

object MuezzinCatalog {
    const val DEFAULT_ID = "الأذان الأساسي · CC0"
    const val DEFAULT_AUDIO = "https://upload.wikimedia.org/wikipedia/commons/e/e7/Adhan.ogg"

    val readyAudioByName: LinkedHashMap<String, String> = linkedMapOf(
        DEFAULT_ID to DEFAULT_AUDIO,
        "أذان 01 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan1.mp3",
        "أذان 02 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan2.mp3",
        "أذان 03 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan3.mp3",
        "أذان 04 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan4.mp3",
        "أذان 05 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan5.mp3",
        "أذان 06 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan6.mp3",
        "أذان 07 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan7.mp3",
        "أذان 08 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan8.mp3",
        "أذان 09 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan9.mp3",
        "أذان 10 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan10.mp3",
        "أذان 11 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan11.mp3",
        "أذان 12 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan12.mp3",
        "أذان 13 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan13.mp3",
        "أذان 14 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan14.mp3",
        "أذان 15 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan15.mp3",
        "أذان 16 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan16.mp3",
        "أذان 17 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan17.mp3",
        "أذان 18 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan18.mp3",
        "أذان 19 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan19.mp3",
        "أذان 20 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan20.mp3",
        "أذان 21 · مكتبة مجانية" to "https://www.islamcan.com/audio/adhan/azan21.mp3"
    )

    val famousNames = arrayOf(
        "الشيخ علي أحمد ملا · مكة",
        "الشيخ عصام بخاري · المدينة",
        "الشيخ محمد مكاوي · مكة",
        "الشيخ نايف فيدة · مكة",
        "الشيخ فاروق حضراوي · مكة",
        "الشيخ أحمد يونس خوجة · مكة",
        "الشيخ محمد يوسف شاكر · المدينة",
        "الشيخ عبد الله باعفيف · مكة",
        "الشيخ فيصل نعمان · المدينة",
        "الشيخ إياد شكري · المدينة"
    )

    val names: Array<String> =
        readyAudioByName.keys.toTypedArray() + famousNames + arrayOf("مؤذن من اختياري")
}
