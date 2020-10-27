package com.jayant.www.jarvis;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    private static final int PERMISSIONS_REQUEST_RECORD_AUDIO = 1;
    private static final String LOG_TAG = MainActivity.class.getSimpleName();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ((Button)findViewById(R.id.btn)).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                stopService(new Intent(MainActivity.this, MyService.class));
                startService(new Intent(MainActivity.this, MyService.class));
                Log.i(LOG_TAG, "onClick");
                int permissionCheck = ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.RECORD_AUDIO);
                if (permissionCheck == PackageManager.PERMISSION_DENIED) {
                    ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.RECORD_AUDIO}, PERMISSIONS_REQUEST_RECORD_AUDIO);
                    return;
                }
            }
        });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        if (requestCode == PERMISSIONS_REQUEST_RECORD_AUDIO) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                stopService(new Intent(MainActivity.this, MyService.class));
                startService(new Intent(MainActivity.this, MyService.class));
            } else {
                finish();
            }
        }
    }
}