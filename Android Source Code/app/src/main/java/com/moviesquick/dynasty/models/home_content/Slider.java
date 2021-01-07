package com.moviesquick.dynasty.models.home_content;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.ArrayList;

public class Slider {
    @SerializedName("slider_type")
    @Expose
    private String sliderType;

   // @TypeConverters(SliderTypeConverter.class)
    @SerializedName("slide")
    @Expose
    private ArrayList<Slide> slideArrayList = null;

    public String getSliderType() {
        return sliderType;
    }

    public void setSliderType(String sliderType) {
        this.sliderType = sliderType;
    }

    public ArrayList<Slide> getSlideArrayList() {
        return slideArrayList;
    }

    public void setSlideArrayList(ArrayList<Slide> slideArrayList) {
        this.slideArrayList = slideArrayList;
    }
}
