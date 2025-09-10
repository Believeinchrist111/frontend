'use client'

import "./home.css";
import ComposeSection from "../ui/compose-section.js";
import TweetCard from "../ui/tweet-card.js"
import HomeNav from "../ui/home-nav.js"
import FooterNav from "../ui/footer-nav.js"
import ToggleSideNav from "../ui/toggle-side-nav";
import SideNav from "../ui/side-nav";


import { useState, useEffect } from "react";
import Link from "next/link";



export default function Home() {
  const [toggleNav, setToggleNav] = useState(false)
  const [togglePost, setTogglePost] = useState(false)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true); // loading state
  const [error, setError] = useState(null);     // error state


  useEffect(() => {
    const fetchUser = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch("/api/users/", {
          headers: { "Content-Type": "application/json" },
          credentials: "include", // important for cookie auth
        });

        if (!response.ok) {
          throw new Error("Failed to fetch user");
        }

        const userData = await response.json();
        setUser(userData);


      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);


  // if (!user) {
  //   return <p>Loading user...</p>;
  // }

  // conditional rendering
  if (loading) return <p>Loading user...</p>;
  if (error) return <p style={{ color: "red" }}>Error: {error}</p>;

  return (
    <>
      <div id="home-body">
        <HomeNav toggleNav={toggleNav} setToggleNav={setToggleNav} />
        <section id="posts-section">
          <ComposeSection />
          <TweetCard user={user} />
          <TweetCard user={user} />
          <TweetCard user={user} />
          <TweetCard user={user} />
        </section>
        <SideNav />
        <FooterNav />
        <ToggleSideNav toggleNav={toggleNav} setToggleNav={setToggleNav} />

        <Link href='/compose/post'>
          <button id="compose-button" onClick={() => setTogglePost(!togglePost)}>
            <svg viewBox="0 0 24 24" className="post-icon" ><g><path d="M23 3c-6.62-.1-10.38 2.421-13.05 6.03C7.29 12.61 6 17.331 6 22h2c0-1.007.07-2.012.19-3H12c4.1 0 7.48-3.082 7.94-7.054C22.79 10.147 23.17 6.359 23 3zm-7 8h-1.5v2H16c.63-.016 1.2-.08 1.72-.188C16.95 15.24 14.68 17 12 17H8.55c.57-2.512 1.57-4.851 3-6.78 2.16-2.912 5.29-4.911 9.45-5.187C20.95 8.079 19.9 11 16 11zM4 9V6H1V4h3V1h2v3h3v2H6v3H4z"></path></g></svg>
          </button>
        </Link>
      </div>
    </>
  );
}

