package com.moviesquick.dynasty.database.homeContent.converters;

import androidx.room.TypeConverter;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.moviesquick.dynasty.models.home_content.PopularStars;

import java.lang.reflect.Type;
import java.util.List;

public class PopularStarsConverter {
    @androidx.room.TypeConverter
    public static String fromArrayList(List<PopularStars> stars){
        Gson gson = new Gson();
        return gson.toJson(stars);
    }

    @TypeConverter
    public static List<PopularStars> jsonToList(String value){
        Type listType = new TypeToken<List<PopularStars>>() {}.getType();

        Gson gson = new Gson();
        return gson.fromJson(value, listType);
    }
}
