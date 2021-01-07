package com.moviesquick.dynasty.database.homeContent;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import com.moviesquick.dynasty.models.home_content.HomeContent;

import static androidx.room.OnConflictStrategy.REPLACE;

@Dao
public interface HomeContentDao {
    @Insert(onConflict = REPLACE)
    void insertHomeContentData(HomeContent homeContent);

    @Update
    void updateHomeContentData(HomeContent homeContent);

    @Query("DELETE FROM home_content_table")
    void deleteAllHomeContentData();

    @Query("SELECT * FROM home_content_table")
    LiveData<HomeContent> getLiveHomeContentData();

    @Query("SELECT * FROM home_content_table")
    HomeContent getHomeContentData();
}
