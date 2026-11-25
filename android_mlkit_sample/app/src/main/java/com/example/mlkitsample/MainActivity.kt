package com.example.mlkitsample

import android.app.Activity
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import com.google.mlkit.vision.common.InputImage
import com.google.mlkit.vision.text.TextRecognition
import com.google.mlkit.vision.text.latin.TextRecognizerOptions

class MainActivity : AppCompatActivity() {

    private val pickImage = registerForActivityResult(ActivityResultContracts.GetContent()) { uri: Uri? ->
        uri?.let { handleImageUri(it) }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // No layout provided — integrate into your activity layout as needed.

        // Example: launch image picker to test
        pickImage.launch("image/*")
    }

    private fun handleImageUri(uri: Uri) {
        val stream = contentResolver.openInputStream(uri) ?: return
        val bitmap = BitmapFactory.decodeStream(stream)
        stream.close()
        runTextRecognition(bitmap)
    }

    private fun runTextRecognition(bitmap: Bitmap) {
        val image = InputImage.fromBitmap(bitmap, 0)
        val recognizer = TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)
        recognizer.process(image)
            .addOnSuccessListener { visionText ->
                val rawText = visionText.text ?: ""
                // Parse CR fields
                val cr = TextParser.parseCR(rawText)
                // Use `cr` (data class) to populate UI or send to backend
                // Example log
                println("CR parse result: $cr")
            }
            .addOnFailureListener { e ->
                e.printStackTrace()
            }
    }
}
