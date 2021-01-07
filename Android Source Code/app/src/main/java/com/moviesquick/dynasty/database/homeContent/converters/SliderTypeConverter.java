package com.moviesquick.dynasty.database.homeContent.converters;

import androidx.room.TypeConverter;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.moviesquick.dynasty.models.home_content.Slider;

import java.lang.reflect.Type;

public class SliderTypeConverter {
    @androidx.room.TypeConverter
    public static String fromArrayList(Slider slider){
        Gson gson = new Gson();
        return gson.toJson(slider);
    }

    @TypeConverter
    public static Slider jsonToList(String value){
        Type listType = new TypeToken<Slider>() {}.getType();

        Gson gson = new Gson();
        return gson.fromJson(value, listType);
    }
}
