"use client";

import Link from "next/link.js";
import { useRouter } from "next/navigation";

import "./post-nav.css"


export default function PostNav() {
 const router = useRouter()

 return (
  <>
   <nav id="post-nav">
    <button className="back-button" onClick={() => router.push('/home')}>
     <svg viewBox="0 0 24 24" className="back-icon"><g><path d="M7.414 13l5.043 5.04-1.414 1.42L3.586 12l7.457-7.46 1.414 1.42L7.414 11H21v2H7.414z"></path></g>
     </svg>
    </button>

    <h1 id="post">Post</h1>
   </nav>
  </>

 );
}
