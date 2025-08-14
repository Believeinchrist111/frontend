'use client'

import "./page.css";
import TweetCard from "./ui/tweet-card.js"
import HomeNav from "./ui/home-nav.js"
import HomeFooterNav from "./ui/home-footer-nav.js"
import SideNav from "./ui/side-nav";

import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import {useRouter} from "next/navigation";


export default function Home() {
  const [toggleNav, setToggleNav] = useState(false)
  const [togglePost, setTogglePost] = useState(false)

  const navigate = useRouter()


  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem('token')
      console.log(token)
      try{
        const response = await fetch(`http://127.0.0.1:8000/login`, {
        headers: {
          Authorization: `Bearer ${token}`,
        }
      });

        if (!response.ok) {
          throw new Error('Token verification failed');
        }
      } catch (error) {
        localStorage.removeItem('token');
        navigate.push('/sign-up-in')
      }
    };

    verifyToken();
  }, [navigate])

  return (
    <>
      <HomeNav toggleNav={toggleNav} setToggleNav={setToggleNav} />
      <section id="posts-section">
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
        <TweetCard />
        <TweetCard />
        <TweetCard />
        <TweetCard />
        <TweetCard />
        <TweetCard />
      </section>
      <HomeFooterNav />
      <SideNav toggleNav={toggleNav} setToggleNav={setToggleNav} />
      <Link href='/compose/post'>
        <button id="compose-button" onClick={() => setTogglePost(!togglePost)}>
          <svg viewBox="0 0 24 24" className="post-icon" ><g><path d="M23 3c-6.62-.1-10.38 2.421-13.05 6.03C7.29 12.61 6 17.331 6 22h2c0-1.007.07-2.012.19-3H12c4.1 0 7.48-3.082 7.94-7.054C22.79 10.147 23.17 6.359 23 3zm-7 8h-1.5v2H16c.63-.016 1.2-.08 1.72-.188C16.95 15.24 14.68 17 12 17H8.55c.57-2.512 1.57-4.851 3-6.78 2.16-2.912 5.29-4.911 9.45-5.187C20.95 8.079 19.9 11 16 11zM4 9V6H1V4h3V1h2v3h3v2H6v3H4z"></path></g></svg>
        </button>
      </Link>
    </>
  );
}

