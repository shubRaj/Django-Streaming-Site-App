package com.moviesquick.dynasty.database.downlaod;

import android.content.Context;

import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;

import com.moviesquick.dynasty.models.DownloadInfo;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Database(entities = {DownloadInfo.class}, exportSchema = false, version = 1)
public abstract class DownloadDatabase extends RoomDatabase {
    private static final String TAG = "DownloadDatabase";

    private static DownloadDatabase instance;
    public abstract DownloadDao downloadDao();
    private static final int NUMBER_OF_THREADS = 4;
    static final ExecutorService databaseWriteExecutor =
            Executors.newFixedThreadPool(NUMBER_OF_THREADS);

    public static synchronized DownloadDatabase getInstance(Context context){
        if (instance == null){
            instance = Room.databaseBuilder(context.getApplicationContext(),
                    DownloadDatabase.class, "Download_DB")
                    .fallbackToDestructiveMigration()
                    .build();
        }

        return instance;
    }
}
