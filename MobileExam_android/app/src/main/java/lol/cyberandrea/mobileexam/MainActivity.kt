package lol.cyberandrea.mobileexam

import android.Manifest
import android.app.Activity
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.icu.text.SimpleDateFormat
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.content.IntentFilter
import com.google.firebase.FirebaseApp
import android.widget.Toast
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import androidx.localbroadcastmanager.content.LocalBroadcastManager
import com.google.firebase.messaging.FirebaseMessaging
import org.json.JSONObject
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import lol.cyberandrea.mobileexam.databinding.ActivityMainBinding
import lol.cyberandrea.mobileexam.db.NotificationDatabaseHelper
import java.util.Date
import java.util.Locale

class MainActivity : Activity() {

    private var SERVER_IP = ""
    private val PREFS_NAME = "AppPrefs"
    private val KEY_SERVER_IP = "server_ip"

    private lateinit var binding: ActivityMainBinding
    private var serviceRunning = false

    companion object {
        private const val REQUEST_CODE_NOTIFICATIONS = 1001
    }

    private val notificationReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            updateNotificationList()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try {
            if (FirebaseApp.getApps(this).any { it.name == FirebaseApp.DEFAULT_APP_NAME }) {
            Log.d("FirebaseInit", "Default FirebaseApp already exists. Not re-initializing.")
            val app = FirebaseApp.getInstance()
            val options = app.options
            Log.d("FirebaseInit", "Existing FirebaseOptions: Project ID=${options.projectId}, App ID=${options.applicationId}, API Key=${options.apiKey}")
            } else {
                val app = FirebaseApp.initializeApp(this)
                FirebaseApp.initializeApp(this)
                Log.d("FirebaseInit", "FirebaseApp initialized successfully in MyApplication.onCreate()")
            }

//          Token Logging
            FirebaseMessaging.getInstance().token
                .addOnCompleteListener { task ->
                    if (!task.isSuccessful) {
                        Log.w("FCM_TOKEN", "Fetching FCM registration token failed", task.exception)
                        return@addOnCompleteListener
                    }

                    val token = task.result
                    Log.d("FCM_TOKEN", "Manual fetch: $token")
                }


        } catch (e: IllegalStateException) {
            Log.e("FirebaseInit", "FirebaseApp already initialized or failed to initialize: ${e.message}")
        } catch (e: Exception) {
            Log.e("FirebaseInit", "Unexpected error during FirebaseApp initialization: ${e.message}")
        }

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Ricevi broadcast da Service
        LocalBroadcastManager.getInstance(this).registerReceiver(
            notificationReceiver, IntentFilter("NEW_NOTIFICATION_RECEIVED")
        )

//        Indirizzo IP SERVER
        val prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        SERVER_IP = prefs.getString(KEY_SERVER_IP, "10.42.0.1") ?: "10.42.0.1"
        binding.ipInput.setText(SERVER_IP)

        binding.saveIpButton.setOnClickListener {
            val newIp = binding.ipInput.text.toString().trim()
            if (newIp.isNotEmpty() && newIp != SERVER_IP) {
                SERVER_IP = newIp
                val prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
                prefs.edit().putString(KEY_SERVER_IP, newIp).apply()
                Toast.makeText(this, "Server IP aggiornato: $SERVER_IP", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "IP non modificato o vuoto", Toast.LENGTH_SHORT).show()
            }
            FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
                if (!task.isSuccessful) {
                    Log.w("Push", "Fetching FCM registration token failed", task.exception)
                    return@addOnCompleteListener
                }
                val token = task.result
                registerTokenWithServer(token)
            }
        }


        askNotificationPermission()

        val db = NotificationDatabaseHelper(this)
        val notifications = db.getAllNotifications()
        val formatted = notifications.joinToString("\n\n") {
            val date = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault())
                .format(Date(it.timestamp))
            "🕒 $date\n📌 ${it.title}\n✉️ ${it.body}"
        }

        binding.textNotifications.text = formatted.ifEmpty { "Nessuna notifica ricevuta." }
    }

    override fun onDestroy() {
        super.onDestroy()
        LocalBroadcastManager.getInstance(this).unregisterReceiver(notificationReceiver)
    }

    private fun registerTokenWithServer(token: String) {
        val json = JSONObject()
        json.put("token", token)

        val url = "http://$SERVER_IP:5000/register"
        val request = JsonObjectRequest(
            com.android.volley.Request.Method.POST,
            url, json,
            { response -> Log.d("Push", "Registered: $response") },
            { error -> Log.e("Push", "Error registering token: $error") }
        )
        Log.d("Push", "Sending token to $url with payload: $json")
        Volley.newRequestQueue(this).add(request)
    }

    private fun updateNotificationList() {
        val db = NotificationDatabaseHelper(this)
        val notifications = db.getAllNotifications()

        val formatted = notifications.joinToString("\n\n") {
            val date = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault())
                .format(Date(it.timestamp))
            "🕒 $date\n📌 ${it.title}\n✉️ ${it.body}"
        }

        binding.textNotifications.text = formatted.ifEmpty { "Nessuna notifica ricevuta." }
    }

    private fun askNotificationPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED) {

                if (ActivityCompat.shouldShowRequestPermissionRationale(this, Manifest.permission.POST_NOTIFICATIONS)) {
                    Toast.makeText(
                        this,
                        "L'app ha bisogno del permesso per mostrarti le notifiche.",
                        Toast.LENGTH_LONG
                    ).show()
                }

                // Chiede il permesso
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                    REQUEST_CODE_NOTIFICATIONS
                )
            }
        }
    }

    // Callback della richiesta
    override fun onRequestPermissionsResult(
        requestCode: Int, permissions: Array<out String>, grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_CODE_NOTIFICATIONS) {
            if ((grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED)) {
                Toast.makeText(this, "Notifiche abilitate", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Permesso notifiche negato", Toast.LENGTH_LONG).show()
            }
        }
    }

}
