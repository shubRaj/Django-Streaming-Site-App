package com.moviesquick.dynasty.network.apis;

import com.moviesquick.dynasty.network.model.config.Configuration;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Header;

public interface ConfigurationApi {

    @GET("config")
    Call<Configuration> getConfigurationData(@Header("API-KEY") String apiKey);
}
