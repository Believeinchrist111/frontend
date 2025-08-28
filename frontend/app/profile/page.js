import Image from "next/image"
import Link from "next/link"

import "./profile.css"

export default function Profile() {

 return (
  <>
   <div id="profile-wrapper">

    <div id="profile-nav">
     <button className="back-button">
      <svg viewBox="0 0 24 24" className="back-icon"><g><path d="M7.414 13l5.043 5.04-1.414 1.42L3.586 12l7.457-7.46 1.414 1.42L7.414 11H21v2H7.414z"></path></g></svg>
     </button>

     <h1 id="username-post-header"><span id="user-name">Emmanuel Nyarko</span><span id="tab-label-number">16</span><span id="active-tab"> posts</span></h1>

     <button id="search-button">
      <svg viewBox="0 0 24 24" className="search-icon" ><g><path d="M10.25 3.75c-3.59 0-6.5 2.91-6.5 6.5s2.91 6.5 6.5 6.5c1.795 0 3.419-.726 4.596-1.904 1.178-1.177 1.904-2.801 1.904-4.596 0-3.59-2.91-6.5-6.5-6.5zm-8.5 6.5c0-4.694 3.806-8.5 8.5-8.5s8.5 3.806 8.5 8.5c0 1.986-.682 3.815-1.824 5.262l4.781 4.781-1.414 1.414-4.781-4.781c-1.447 1.142-3.276 1.824-5.262 1.824-4.694 0-8.5-3.806-8.5-8.5z"></path></g></svg>
     </button>
    </div>

    <div id="profile-image-banner">
    </div>

    <div id="profile-container">

     <Image
      src="/emma.jpeg"
      height={40}
      width={40}
      className="profile-page-image"
      alt="profile-page-image"
     />
     <button id="edit-profile-button">Edit profile</button>

     <div id="handle-container">
      <div id="user-name">Emmanuel Nyarko</div>
      <div id="user-account-name">@Emmakoko</div>
      <div id="date-joined">
       <svg viewBox="0 0 24 24" className="date-icon"><g><path d="M7 4V3h2v1h6V3h2v1h1.5C19.89 4 21 5.12 21 6.5v12c0 1.38-1.11 2.5-2.5 2.5h-13C4.12 21 3 19.88 3 18.5v-12C3 5.12 4.12 4 5.5 4H7zm0 2H5.5c-.27 0-.5.22-.5.5v12c0 .28.23.5.5.5h13c.28 0 .5-.22.5-.5v-12c0-.28-.22-.5-.5-.5H17v1h-2V6H9v1H7V6zm0 6h2v-2H7v2zm0 4h2v-2H7v2zm4-4h2v-2h-2v2zm0 4h2v-2h-2v2zm4-4h2v-2h-2v2z"></path></g></svg>Joined August 2025
      </div>

      <div id="following-followers-container">
       <button><span id="following-number">31</span> Following</button>
       <button><span id="followers-number">10</span> Followers</button>
      </div>
     </div>
    </div>

    <div id="profile-tab-nav">
     <span>Posts</span>
     <span>Replies</span>
     <span>Highlights</span>
     <span>Articles</span>
     <span>Media</span>
     <span>Likes</span>
    </div>
   </div>
  </>
 );
}
