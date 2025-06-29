package lol.cyberandrea.mobileexam

import android.content.Intent
import android.app.NotificationChannel
import android.app.NotificationManager
import androidx.localbroadcastmanager.content.LocalBroadcastManager
import android.app.Service
import android.content.Context
import android.os.Build
import android.util.Log
import androidx.core.app.NotificationCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import lol.cyberandrea.mobileexam.db.NotificationDatabaseHelper

class MyFirebaseService : FirebaseMessagingService() {

    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        val title = remoteMessage.notification?.title ?: "Notifica"
        val body = remoteMessage.notification?.body ?: "Hai un nuovo messaggio"
        Log.d("MyFirebaseService","Received a notification")

        val db = NotificationDatabaseHelper(this)
        Log.d("MyFirebaseService","Saving the notification")
        db.insertNotification(title, body)

        val intent = Intent("NEW_NOTIFICATION_RECEIVED")
        LocalBroadcastManager.getInstance(this).sendBroadcast(intent)

        // Manda notifica su schermo
        showNotification(title, body)
    }

    private fun showNotification(title: String, body: String) {
        val channelId = "push_channel"
        val notificationManager =
            getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(channelId, "Notifiche Push",
                NotificationManager.IMPORTANCE_DEFAULT)
            notificationManager.createNotificationChannel(channel)
        }

        val notification = NotificationCompat.Builder(this, channelId)
            .setContentTitle(title)
            .setContentText(body)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .build()

        notificationManager.notify(1, notification)
    }
}
