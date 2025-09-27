"use client";

import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { createPost } from "../lib/slices/postSlice";
import Image from "next/image";
import { Smile, Image as ImageIcon } from "lucide-react";

import "./compose-section.css"

export default function ComposeSection() {
 const [content, setContent] = useState("");
 const [media, setMedia] = useState([]);
 const dispatch = useDispatch();
 const { loading, error } = useSelector((state) => state.posts);

 // Handle multiple uploads
 const handleMediaChange = (e) => {
  const files = Array.from(e.target.files);
  const newMedia = files.map((file) => ({
   file,
   preview: URL.createObjectURL(file),
  }));
  setMedia((prev) => [...prev, ...newMedia]);
 };

 // Remove single file
 const removeMedia = (index) => {
  setMedia((prev) => prev.filter((_, i) => i !== index));
 };


 const handlePost = () => {
  if (!content.trim() && media.length === 0) {
   alert("Post must have at least content or media.");
   return;
  }

  dispatch(createPost({ content, media }))
   .unwrap()
   .then(() => {
    setContent("");
    setMedia([]);
   })
   .catch((err) => {
    console.error("Failed to post:", err);
   });
 };


 return (
  <div id="compose-section">

   <div id="textarea-container">

    <div id="textarea-img-container">
     <Image
      className="profile-img"
      src={"/emma.jpeg"}
      height={40}
      width={40}
      alt="profile-image"
     />

     <textarea
      placeholder="What’s happening?"
      value={content}
      onChange={(e) => setContent(e.target.value)}
      className="post-textarea"
      rows={3}
     />
    </div>

    {/* Media preview */}
    {media.length > 0 && (
     <div className="media-grid">
      {media.map((m, index) => (
       <div key={index} className="media-item">
        {m.file.type.startsWith("image/") ? (
         <img src={m.preview} alt="preview" />
        ) : (
         <video src={m.preview} controls />
        )}
        <button
         className="remove-media"
         onClick={() => removeMedia(index)}
        >
         {/* <X size={18} /> */}
        </button>
       </div>
      ))}
     </div>
    )}

    <div className="compose-sec-toolbar">
     <div className="tools-left">
      <label className="icon-btn">
       <input
        type="file"
        accept="image/*,video/*"
        hidden
        multiple
        onChange={handleMediaChange}
       />
       <ImageIcon size={20} />
      </label>
      <button type="button" className="icon-btn">
       <Smile size={20} />
      </button>
     </div>

     <button
      id="post-button"
      onClick={handlePost}
      disabled={!content.trim() && !media.length}>
      Post
     </button>
    </div>
   </div>
  </div>
 )
}


{/* <button
 className={`post-btn ${content.trim() || media.length ? "active" : ""}`}
 onClick={handlePost}
 disabled={!content.trim() && !media.length}
>
 Post
</button> */}