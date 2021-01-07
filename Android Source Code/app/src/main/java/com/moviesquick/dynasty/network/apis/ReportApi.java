package com.moviesquick.dynasty.network.apis;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.Header;
import retrofit2.http.POST;

public interface ReportApi {
    @FormUrlEncoded
    @POST("report")
    Call<ResponseBody> submitReport(@Header("API-KEY") String apiKey,
                                    @Field("type") String type,
                                    @Field("id") String id,
                                    @Field("video") String video,
                                    @Field("audio") String audio,
                                    @Field("subtitle") String subtitle,
                                    @Field("message") String message
    );
}
