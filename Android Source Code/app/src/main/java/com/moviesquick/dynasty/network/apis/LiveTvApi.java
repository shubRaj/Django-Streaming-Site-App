package com.moviesquick.dynasty.network.apis;

import com.moviesquick.dynasty.network.model.Channel;
import com.moviesquick.dynasty.network.model.LiveTvCategory;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.Query;

public interface LiveTvApi {

    @GET("all_tv_channel_by_category")
    Call<List<LiveTvCategory>> getLiveTvCategories(@Header("API-KEY") String apiKey);

    @GET("featured_tv_channel")
    Call<List<Channel>> getFeaturedTV(@Header("API-KEY") String apiKey,
                                      @Query("page") int page);

}