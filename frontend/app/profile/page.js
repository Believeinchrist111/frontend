'use client'

import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import ProfileNav from "../ui/profile-nav.js";
import ProfileInfoSection from "../ui/profile-info.js"
import TweetCard from "../ui/tweet-card.js";
import FooterNav from "../ui/footer-nav.js"
import SideNav from "../ui/side-nav.js";
import "./profile.css"

import { fetchUser } from "../lib/slices/userSlice";



export default function Profile() {
  const dispatch = useDispatch()
  const { user, loading, error } = useSelector((state) => state.user);

  useEffect(() => {
    dispatch(fetchUser())
  }, [dispatch]);

  if (!user) return <p>Loading...</p>;

  return (
    <>
      <div id="profile-body">
        <div id="profile-wrapper">
          <ProfileNav user={user} />
          <ProfileInfoSection user={user} />
          <TweetCard user={user}/>
          <TweetCard user={user}/>
          <TweetCard user={user}/>
          <TweetCard user={user}/>
        </div>
        <SideNav user={user} />
        <FooterNav />
      </div>
    </>
  );
}
