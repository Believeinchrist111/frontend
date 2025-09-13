'use client'

import Image from "next/image"
import { useState } from "react";


import "./profile-info.css"

export default function ProfileInfoSection({user}) {
 const tabs = ["Posts", "Replies", "Highlights", "Articles", "Media", "Likes"];
 const [activeTab, setActiveTab] = useState("Posts");

 return (
  <>
   <section id="profile-info-section">
    <div id="profile-image-banner">
    </div>

    <button id="edit-profile-button">Edit profile</button>

    <div id="profile-container">
     <Image
      src="/emma.jpeg"
      height={40}
      width={40}
      className="profile-page-image"
      alt="profile-page-image"
     />

     <div id="handle-container">
      <div id="user-name">{user.firstname} {user.lastname}</div>
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
     {tabs.map((tab) => (
      <span
       key={tab}
       className={activeTab === tab ? "active" : ""}
       onClick={() => setActiveTab(tab)}
      >
       {tab}
      </span>
     ))}
    </div>
   </section>

  </>
 )
}