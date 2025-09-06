import Image from "next/image"

import "./home-nav.css"

export default function HomeNav({ toggleNav, setToggleNav }) {
 return (
  <nav id="home-nav">
   <div id="menu-container">
    <div id="menu-image" onClick={() => { setToggleNav(!toggleNav) }}>
     <Image
      src="/emma.jpeg"
      height={40}
      width={40}
      className="profile-image"
      alt="profile-image"
     />
    </div>

    <div id="logo">logo</div>
   </div>

   <div id="for-follow-tabs">
    <button>For you</button>
    <button>Following</button>
   </div>
  </nav>
 )
}



