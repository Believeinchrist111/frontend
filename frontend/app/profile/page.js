import FooterNav from "../ui/footer-nav.js"
import SideNav from "../ui/side-nav.js";
import ProfileInfoSection from "../ui/profile-info-section.js"
import "./profile.css"

export default function Profile() {
 return (
  <>
   <div id="profile-body">
    <div id="profile-wrapper">
     <ProfileInfoSection />
    </div>
     <SideNav />
     <FooterNav />
   </div>
  </>
 );
}
