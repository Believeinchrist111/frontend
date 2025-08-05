import Image from "next/image";
import Link from "next/link";
import "./page.css"


export default function Post() {

 return (
  <div id="post-component">
   <nav>
    <Link
     href="/">
     <button id="return-button">
      <svg viewBox="0 0 24 24" className=""><g><path d="M7.414 13l5.043 5.04-1.414 1.42L3.586 12l7.457-7.46 1.414 1.42L7.414 11H21v2H7.414z"></path></g></svg>
     </button></Link>
    <button id="post-button">Post</button>

   </nav>
   <div>
    <Image
     className="textarea-profile-image"
     src={'/emma.jpeg'}
     height={40}
     width={40}
     alt="profile-image"
    />
    <textarea placeholder="What’s happening?" className="post-textarea" ></textarea>
   </div>
  </div>

 );
}