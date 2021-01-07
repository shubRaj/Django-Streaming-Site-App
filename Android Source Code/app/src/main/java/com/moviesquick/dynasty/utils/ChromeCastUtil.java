package com.moviesquick.dynasty.utils;

import android.content.Context;

import androidx.mediarouter.app.MediaRouteButton;

import com.google.android.exoplayer2.ext.cast.CastPlayer;
import com.google.android.gms.cast.framework.CastButtonFactory;
import com.google.android.gms.cast.framework.CastContext;

public class ChromeCastUtil implements CastPlayer.SessionAvailabilityListener {

    private CastContext castContext;
    private static CastPlayer castPlayer;

    public void initCast(MediaRouteButton mediaRouteButton, Context context) {
        CastButtonFactory.setUpMediaRouteButton(context.getApplicationContext(), mediaRouteButton);
        castContext = CastContext.getSharedInstance(context);
        castPlayer = new CastPlayer(castContext);
        castPlayer.setSessionAvailabilityListener(this);

    }

    @Override
    public void onCastSessionAvailable() {

    }

    @Override
    public void onCastSessionUnavailable() {

    }
}
