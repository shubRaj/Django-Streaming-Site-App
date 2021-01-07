package com.moviesquick.dynasty.adapters;

import android.content.Context;
import android.content.Intent;

import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.balysv.materialripple.MaterialRippleLayout;
import com.moviesquick.dynasty.DetailsActivity;
import com.moviesquick.dynasty.LoginActivity;
import com.moviesquick.dynasty.R;
import com.moviesquick.dynasty.models.CommonModels;

import com.moviesquick.dynasty.utils.ItemAnimation;
import com.moviesquick.dynasty.utils.PreferenceUtils;
import com.squareup.picasso.Picasso;

import java.util.ArrayList;
import java.util.List;

public class CommonGridAdapter extends RecyclerView.Adapter<CommonGridAdapter.OriginalViewHolder> {

    private List<CommonModels> items = new ArrayList<>();
    private Context ctx;

    private int lastPosition = -1;
    private boolean on_attach = true;
    private int animation_type = 2;


    public CommonGridAdapter(Context context, List<CommonModels> items) {
        this.items = items;
        ctx = context;
    }


    @Override
    public CommonGridAdapter.OriginalViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {

        CommonGridAdapter.OriginalViewHolder vh;
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_grid_image_albums, parent, false);
        vh = new OriginalViewHolder(v);
        return vh;

    }

    @Override
    public void onBindViewHolder(CommonGridAdapter.OriginalViewHolder holder, final int position) {
        final CommonModels obj = items.get(position);

        holder.qualityTv.setText(obj.getQuality());
        holder.releaseDateTv.setText(obj.getReleaseDate());
        holder.name.setText(obj.getTitle());

        Picasso.get().load(obj.getImageUrl()).placeholder(R.drawable.poster_placeholder).into(holder.image);

        holder.lyt_parent.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (PreferenceUtils.isMandatoryLogin(ctx)){
                    if (PreferenceUtils.isLoggedIn(ctx)){
                        goToDetailsActivity(obj);
                    }else {
                        ctx.startActivity(new Intent(ctx, LoginActivity.class));
                    }
                }else {
                    goToDetailsActivity(obj);
                }
            }
        });

        setAnimation(holder.itemView, position);


    }



    private void goToDetailsActivity(CommonModels obj) {
        Intent intent=new Intent(ctx,DetailsActivity.class);
        intent.putExtra("vType",obj.getVideoType());
        intent.putExtra("id",obj.getId());
        ctx.startActivity(intent);
    }

    @Override
    public int getItemCount() {
        return items.size();
    }

    public class OriginalViewHolder extends RecyclerView.ViewHolder {

        public ImageView image;
        public TextView name, qualityTv, releaseDateTv;
        public MaterialRippleLayout lyt_parent;

        public View view;

        public CardView cardView;

        public OriginalViewHolder(View v) {
            super(v);
            view = v;
            image = v.findViewById(R.id.image);
            name = v.findViewById(R.id.name);
            lyt_parent = v.findViewById(R.id.lyt_parent);
            qualityTv = v.findViewById(R.id.quality_tv);
            releaseDateTv = v.findViewById(R.id.release_date_tv);
            cardView = v.findViewById(R.id.top_layout);
        }

    }


    @Override
    public void onAttachedToRecyclerView(RecyclerView recyclerView) {

        recyclerView.addOnScrollListener(new RecyclerView.OnScrollListener() {
            @Override
            public void onScrollStateChanged(RecyclerView recyclerView, int newState) {
                on_attach = false;
                super.onScrollStateChanged(recyclerView, newState);
            }

        });

        super.onAttachedToRecyclerView(recyclerView);
    }

    private void setAnimation(View view, int position) {
        if (position > lastPosition) {
            ItemAnimation.animate(view, on_attach ? position : -1, animation_type);
            lastPosition = position;
        }
    }

}