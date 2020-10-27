package com.jayant.www.jarvis;

import android.Manifest;
import android.app.Notification;
import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.hardware.Camera;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.BatteryManager;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.os.Environment;
import android.os.Handler;
import android.os.IBinder;
import android.os.PowerManager;
import android.provider.ContactsContract;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.tts.TextToSpeech;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.NotificationCompat;
import android.util.Log;
import android.view.Window;
import android.view.WindowManager;

import java.io.File;
import java.io.FilenameFilter;
import java.lang.reflect.Array;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.Locale;
import java.util.Random;

import static android.content.ContentValues.TAG;

public class MyService extends Service implements
        TextToSpeech.OnInitListener {

    private int i = 0;
    private String songList[] = new String[100];

    private SpeechRecognizer mSpeechRecognizer;
    private Intent mSpeechRecognizerIntent;
    private TextToSpeech tts;
    private String speak;
    private Handler mHandler;
    private AudioManager audioManager;

    private MediaPlayer mpintro;

    private String previous1 = "null";
    private String previous2 = "null";

    private BroadcastReceiver batteryLevel;
    private Camera camera;
    private boolean flash = false;
    private String jokes[] = {"Mother : Anton, do you think I’m a bad mother? Son : My name is Paul.","My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away."};

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // TODO Auto-generated method stub
        audioManager = (AudioManager) this.getSystemService(Context.AUDIO_SERVICE);

        mSpeechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
        tts = new TextToSpeech(this, this);

        this.mHandler = new Handler();
        this.mHandler.postDelayed(m_Runnable, 100);

        startNotification();

        SimpleDateFormat sdf = new SimpleDateFormat("EEEE");
        Date d = new Date();
        String dayOfTheWeek = sdf.format(d);
        if (dayOfTheWeek.equalsIgnoreCase("thursday")){Log.d("cmd:", "thursday"); updates();}

        return super.onStartCommand(intent, flags, startId);
    }

    private void updates() {
        speakOut("Jayant  can you please help me update our playlist");
    }

    private void startNotification() {
        Notification notification = new NotificationCompat.Builder(this)
                .setContentTitle("Karen")
                .setTicker("Karen")
                .setContentText("Status: Online")
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentIntent(null)
                .setOngoing(true)
                .build();
        startForeground(9999, notification);
    }

    private void playSong(String song){
        mpintro = MediaPlayer.create(this, Uri.parse(Environment.getExternalStorageDirectory().getPath()+ "/Music/" + song + ".mp3"));
        mpintro.setLooping(true);
    }
    private void searchMP3() {
        File dir =new File(Environment.getExternalStorageDirectory().getPath()+ "/Music/");
        if (dir.exists()&&dir.isDirectory()){
            File[] files = dir.listFiles(new FilenameFilter(){
                @Override
                public boolean accept(File dir,String name){
                    if(name.contains(".mp3")){
                        Log.d("Name:", name);
                        songList[i] = name;
                        i++;
                    }
                    return name.contains(".mp3");
                }
            });
        }
    }

    private final Runnable m_Runnable = new Runnable() {
        public void run() {
            mSpeechRecognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
            mSpeechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                    RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
            mSpeechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE,
                    Locale.getDefault());

            batteryLevel = new BroadcastReceiver() {
                public void onReceive(Context context, Intent intent) {
                    context.unregisterReceiver(this);
                    int currentLevel = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1);
                    int scale = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1);
                    int chargeState = intent.getIntExtra(BatteryManager.EXTRA_STATUS, -1);
                    int level = -1;
                    if (currentLevel >= 0 && scale > 0) {
                        level = (currentLevel * 100) / scale;
                    }
                    if(level<=10) {
                        speakOut("Your device is low on battery");
                    }
                }
            };

            mSpeechRecognizer.setRecognitionListener(new RecognitionListener() {
                @Override
                public void onReadyForSpeech(Bundle bundle) {

                }

                @Override
                public void onBeginningOfSpeech() {

                }

                @Override
                public void onRmsChanged(float v) {

                }

                @Override
                public void onBufferReceived(byte[] bytes) {

                }

                @Override
                public void onEndOfSpeech() {

                }

                @Override
                public void onError(int i) {

                }

                @Override
                public void onResults(Bundle bundle) {
                    //getting all the matches
                    ArrayList<String> matches = bundle
                            .getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);


                    Log.d("previous:", previous1);

                    //displaying the first match
                    if (matches != null) {
                        Log.d("cmd:", matches.get(0));
                        if (matches.get(0).equalsIgnoreCase("hi karen") || matches.get(0).equalsIgnoreCase("hello karen")
                                || matches.get(0).equalsIgnoreCase("hi kiran") || matches.get(0).equalsIgnoreCase("hello kiran") ) {
                            String ans[] = {"Hello Jayant", "hey Jayant", "hi Jayant"};
                            Random rand=new Random();
                            int x = rand.nextInt(2);
                            speakOut(ans[x]);
                        }
                        if(matches.get(0).equalsIgnoreCase("hey karen") || matches.get(0).equalsIgnoreCase("hey kiran")){
                            speakOut("yes?");
                        }
                        if (matches.get(0).contains("what's the time") || matches.get(0).contains("whats the time") || matches.get(0).contains("what is the time") || matches.get(0).contains("what time is it")){
                            SimpleDateFormat ap = new SimpleDateFormat("hh:mm aa");
                            Date t = new Date();
                            String dayTime = ap.format(t);
                            speakOut("the time is " + dayTime);
                        }
                        if (matches.get(0).contains("what's the date") || matches.get(0).contains("whats the date") || matches.get(0).contains("what is the date")){
                            SimpleDateFormat ap = new SimpleDateFormat("dd MMMMMMMMM yyyy");
                            Date t = new Date();
                            String date = ap.format(t);
                            speakOut("today is " + date);
                        }
                        if (matches.get(0).contains("what's up karen")||matches.get(0).contains("what's up Karen") || matches.get(0).contains("what's up kiran")||matches.get(0).contains("what's up Kiran")
                                || matches.get(0).contains("WhatsApp karen")||matches.get(0).contains("WhatsApp Karen") || matches.get(0).contains("WhatsApp kiran")||matches.get(0).contains("WhatsApp Kiran")){
                            speakOut("nothing much");
                        }
                        if (matches.get(0).contains("what were you doing") || matches.get(0).contains("what are you doing")) {
                            String ans[] = {"I was just studying", "checking out our playlist", "I was surfing on web", "reading books"};
                            Random rand=new Random();
                            int x = rand.nextInt(3);
                            speakOut(ans[x]);
                        }
                        if (matches.get(0).contains("where are you") || matches.get(0).contains("where were you")) {
                            String ans[] = {"always by your side", "in your mind"};
                            Random rand=new Random();
                            int x = rand.nextInt(1);
                            speakOut(ans[x]);
                        }
                        if (matches.get(0).contains("do you know") && matches.get(0).contains("joke")) {
                            speakOut("yes. would you like to listen to some");
                        }
                        if (previous1.contains("do you know") && previous1.contains("joke")  || previous1.contains("would you like to listen to some")) {
                            if (matches.get(0).contains("yes") || matches.get(0).contains("yeah") || matches.get(0).contains("sure")) {
                                Random rand = new Random();
                                int count = jokes.length;
                                int x = rand.nextInt(count - 1);
                                speakOut(jokes[x]);
                            }
                        }
                        if (matches.get(0).contains("turn on") && (matches.get(0).contains("flash") || matches.get(0).contains("torch")) ) {
                            speakOut("flash is on");
                            startFlash();
                        }
                        if (matches.get(0).contains("turn off") || matches.get(0).contains("turn it off") && flash==true) {
                            speakOut("okay");
                            closeFlash();
                        }

                        if (matches.get(0).contains("play song") || matches.get(0).contains("play music")) {
                            speakOut("playing music");
                            searchMP3();
                            Random rand = new Random();
                            int x = rand.nextInt(i);
                            String chosen = songList[x].substring(0, songList[x].length() - 4);

                            Log.d("Chosen:", chosen);
                            playSong(chosen);
                            mpintro.start();
                        }
                        else if (matches.get(0).contains("play")) {
                            String cmd = matches.get(0);
                            String song = cmd.substring(cmd.lastIndexOf(" ") + 1);
                            speakOut("playing"+song);
                            playSong(song);
                            mpintro.start();
                        }
                        if (matches.get(0).contains("stop music") || matches.get(0).contains("stop song") || matches.get(0).contains("stop playing")) {
                            speakOut("Okay");
                            mpintro.stop();

                        }

                        if (matches.get(0).contains("call")) {
                            String cmd = matches.get(0);
                            String lastWord = cmd.substring(cmd.lastIndexOf(" ") + 1);
                            getPhoneNumber(lastWord, MyService.this);
                        }
                        if (matches.get(0).contains("slow")) {
                            String ans[] = {"sorry", "I'm sorry"};
                            Random rand=new Random();
                            int x = rand.nextInt(1);
                            speakOut(ans[x]);
                        }
                        if (matches.get(0).contains("shutdown")) {
                            shutdown();
                        }
                        if (matches.get(0).contains("mute")) {
                            mute();
                        }
                        if (matches.get(0).contains("speak")) {
                            unmute();
                        }

                        previous2 = previous1;
                        previous1 = matches.get(0);
                        Log.d("previous:", previous1);
                    }
                }

                @Override
                public void onPartialResults(Bundle bundle) {

                }

                @Override
                public void onEvent(int i, Bundle bundle) {

                }
            });

            mSpeechRecognizer.startListening(mSpeechRecognizerIntent);

            mHandler.postDelayed(m_Runnable, 100);
        }
    };

    public MyService() {
    }

    public void startFlash() {
        camera = Camera.open();
        Camera.Parameters parameters1 = camera.getParameters();
        parameters1.setFlashMode(Camera.Parameters.FLASH_MODE_TORCH);
        camera.setParameters(parameters1);
        camera.startPreview();
        flash = true;
    }
    public void closeFlash() {
        Camera.Parameters parameters2 = camera.getParameters();
        parameters2.setFlashMode(Camera.Parameters.FLASH_MODE_OFF);
        camera.setParameters(parameters2);
        camera.stopPreview();
        camera.release();
        flash = false;
    }

    public void call(String number) {
        Log.d("call", number);
        Intent callIntent = new Intent(Intent.ACTION_CALL);
        callIntent.setData(Uri.parse("tel:" + number)).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }
        startActivity(callIntent);
    }
    public String getPhoneNumber(String name, Context context) {
        String ret = null;
        String selection = ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME+" like'%" + name +"%'";
        String[] projection = new String[] { ContactsContract.CommonDataKinds.Phone.NUMBER};
        Cursor c = context.getContentResolver().query(ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                projection, selection, null, null);
        if (c.moveToFirst()) {
            ret = c.getString(0);
            Log.d("no", ret);
            call(ret);
            speakOut("calling" + name);
        }
        c.close();
        if(ret==null)
            ret = "Unsaved";
        return ret;
    }

    public void sleep() {
        PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE);
    }
    public void shutdown() {
        mSpeechRecognizer.stopListening(); mSpeechRecognizer.destroy(); tts.stop();
        stopService(new Intent(this, MyService.class));
    }
    public void mute() {
        audioManager.setStreamVolume(AudioManager.STREAM_MUSIC, 0, 0);
    }
    public void unmute() {
        audioManager.setStreamVolume(AudioManager.STREAM_MUSIC, 50, 0);
    }

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
    }

    @Override
    public void onInit(int status) {
        if (status == TextToSpeech.SUCCESS) {
            int result = tts.setLanguage(Locale.US);
            if (result == TextToSpeech.LANG_MISSING_DATA
                    || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                Log.e("TTS", "This Language is not supported");
            } else {
                speakOut("");
            }
        } else {
            Log.e("TTS", "Initilization Failed!");
        }
    }
    private void speakOut(String answer) {

        tts.speak(answer, TextToSpeech.QUEUE_FLUSH, null);


    }
}
