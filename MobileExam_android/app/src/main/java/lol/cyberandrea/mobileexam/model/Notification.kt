package lol.cyberandrea.mobileexam.db

data class Notification(
    val id: Int,
    val title: String,
    val body: String,
    val timestamp: Long
)
