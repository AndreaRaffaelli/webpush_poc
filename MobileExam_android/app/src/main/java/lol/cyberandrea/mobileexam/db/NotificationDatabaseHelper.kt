package lol.cyberandrea.mobileexam.db

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper

class NotificationDatabaseHelper(context: Context) :
    SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {

    companion object {
        private const val DATABASE_NAME = "notifications.db"
        private const val DATABASE_VERSION = 1
        const val TABLE_NAME = "notifications"
        const val COLUMN_ID = "id"
        const val COLUMN_TITLE = "title"
        const val COLUMN_BODY = "body"
        const val COLUMN_TIMESTAMP = "timestamp"
    }

    override fun onCreate(db: SQLiteDatabase) {
        val createTable = """
            CREATE TABLE $TABLE_NAME (
                $COLUMN_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                $COLUMN_TITLE TEXT,
                $COLUMN_BODY TEXT,
                $COLUMN_TIMESTAMP INTEGER
            )
        """
        db.execSQL(createTable)
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        db.execSQL("DROP TABLE IF EXISTS $TABLE_NAME")
        onCreate(db)
    }

    fun insertNotification(title: String, body: String) {
        val db = writableDatabase
        val values = ContentValues().apply {
            put(COLUMN_TITLE, title)
            put(COLUMN_BODY, body)
            put(COLUMN_TIMESTAMP, System.currentTimeMillis())
        }
        db.insert(TABLE_NAME, null, values)
        db.close()
    }

    fun getAllNotifications(): List<Notification> {
        val notifications = mutableListOf<Notification>()
        val db = readableDatabase
        val cursor = db.query(
            TABLE_NAME, null, null, null, null, null,
            "$COLUMN_TIMESTAMP DESC"
        )

        with(cursor) {
            while (moveToNext()) {
                notifications.add(
                    Notification(
                        getInt(getColumnIndexOrThrow(COLUMN_ID)),
                        getString(getColumnIndexOrThrow(COLUMN_TITLE)),
                        getString(getColumnIndexOrThrow(COLUMN_BODY)),
                        getLong(getColumnIndexOrThrow(COLUMN_TIMESTAMP))
                    )
                )
            }
            close()
        }
        db.close()
        return notifications
    }
}
