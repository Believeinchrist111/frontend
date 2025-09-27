'use client'

import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Link from "next/link";

import "./home.css";
import ComposeSection from "../ui/compose-section.js";
import TweetCard from "../ui/tweet-card.js"
import HomeNav from "../ui/home-nav.js"
import FooterNav from "../ui/footer-nav.js"
import ToggleSideNav from "../ui/toggle-side-nav";
import SideNav from "../ui/side-nav";

import { fetchUser } from "../lib/slices/userSlice";
import { fetchPosts } from "../lib/slices/postSlice";


export default function Home() {
  const [toggleNav, setToggleNav] = useState(false)
  const [togglePost, setTogglePost] = useState(false)

  const dispatch = useDispatch()
  const { user, loading, error } = useSelector((state) => state.user);
  const { posts } = useSelector((state) => state.posts)

  useEffect(() => {
    dispatch(fetchUser())
    dispatch(fetchPosts())
  }, [dispatch]);

  // conditional rendering

  if (!user) return <p>Loading...</p>;
  if (loading) return <p>Loading user...</p>;
  if (error) return <p style={{ color: "red" }}>Error: {error}</p>;

  return (
    <>
      <div id="home-body">
        <HomeNav toggleNav={toggleNav} setToggleNav={setToggleNav} />
        <section id="posts-section">
          <ComposeSection />
          {posts.map((postInfo) => (
            <div key={postInfo.id} className="border-b p-4">
              <TweetCard postInfo={postInfo} />
            </div>
          ))}
        </section>
        <SideNav user={user} />
        <FooterNav />
        <ToggleSideNav toggleNav={toggleNav} setToggleNav={setToggleNav} user={user} />

        <Link href='/compose/post'>
          <button id="compose-button" onClick={() => setTogglePost(!togglePost)}>
            <svg viewBox="0 0 24 24" className="post-icon" ><g><path d="M23 3c-6.62-.1-10.38 2.421-13.05 6.03C7.29 12.61 6 17.331 6 22h2c0-1.007.07-2.012.19-3H12c4.1 0 7.48-3.082 7.94-7.054C22.79 10.147 23.17 6.359 23 3zm-7 8h-1.5v2H16c.63-.016 1.2-.08 1.72-.188C16.95 15.24 14.68 17 12 17H8.55c.57-2.512 1.57-4.851 3-6.78 2.16-2.912 5.29-4.911 9.45-5.187C20.95 8.079 19.9 11 16 11zM4 9V6H1V4h3V1h2v3h3v2H6v3H4z"></path></g></svg>
          </button>
        </Link>
      </div>
    </>
  );
}

