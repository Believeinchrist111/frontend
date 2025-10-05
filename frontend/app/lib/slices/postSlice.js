import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

// Thunk: Fetch a post from backend
export const getPost = createAsyncThunk('posts/getPost', async (id) => {
  const res = await fetch(`/api/posts/${id}`, {
    cache: "no-store", // Always fetch fresh data
  });

  if (!res.ok) {
    throw new Error("Failed to fetch post");
  }

  const data = await res.json();
  return data;
})

// Thunk: Fetch posts from backend
export const fetchPosts = createAsyncThunk("posts/fetchPosts", async () => {
  const res = await fetch("/api/posts", { credentials: "include" });
  if (!res.ok) throw new Error("Failed to fetch posts");
  return await res.json();
});

// Thunk for creating a new post
export const createPost = createAsyncThunk(
  "posts/createPost",
  async ({ content, media }, { rejectWithValue }) => {
    try {
      // Step 1: Upload files if any
      let uploadedMediaItems = [];
      if (media.length > 0) {
        const formData = new FormData();
        media.forEach((m) => formData.append("files", m.file));

        const uploadRes = await fetch("http://127.0.0.1:8000/upload-media", {
          method: "POST",
          body: formData,
        });

        if (!uploadRes.ok) {
          throw new Error("Failed to upload media");
        }

        const uploadData = await uploadRes.json();
        uploadedMediaItems = uploadData.media_items; // [{ file_url, type }]
      }

      // Step 2: Create the post with uploaded media
      const response = await fetch("/api/posts/create_post", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // ensures cookie is sent
        body: JSON.stringify({
          content,
          reply_to_post_id: null,
          repost_of_post_id: null,
          is_repost: false,
          media_items: uploadedMediaItems.length > 0 ? uploadedMediaItems : null,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to create post");
      }

      const data = await response.json();
      return data; // resolved value available in fulfilled reducer
    } catch (err) {
      return rejectWithValue(err.message || "Something went wrong");
    }
  }
);

const postSlice = createSlice({
  name: "posts",
  initialState: {
    post: null,
    replyTarget: null,
    posts: [],       // all posts
    loading: false, // whether fetching or creating is happening
    error: null,    // error messages
  },
  reducers: {
    setReplyTarget: (state, action) => {
      state.replyTarget = action.payload
    },

    clearReplyTarget: (state) => {
      state.replyTarget = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch a post
      .addCase(getPost.pending, (state) => {
        state.loading = true;
      })
      .addCase(getPost.fulfilled, (state, action) => {
        state.loading = false;
        state.post = action.payload;
      })
      .addCase(getPost.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })

      // Fetch posts
      .addCase(fetchPosts.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchPosts.fulfilled, (state, action) => {
        state.loading = false;
        state.posts = action.payload;
      })
      .addCase(fetchPosts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })

      // Create post
      .addCase(createPost.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createPost.fulfilled, (state, action) => {
        state.loading = false;
        state.posts.unshift(action.payload); // add new post to top
      })
      .addCase(createPost.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});


export const { setReplyTarget, clearReplyTarget } = postSlice.actions;
export default postSlice.reducer;
