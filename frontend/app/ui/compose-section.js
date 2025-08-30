import Image from "next/image";

import "./compose-section.css"

export default function ComposeSection() {

 return (
  <div id="compose-section">
   <div id="textarea-container">
    <Image
     className="textarea-profile-image"
     src={'/emma.jpeg'}
     height={40}
     width={40}
     alt="profile-image"
    />
    <textarea placeholder="What’s happening?" className="post-textarea" ></textarea>
    <button id="post-button">Post</button>
   </div>
  </div>
 )
}