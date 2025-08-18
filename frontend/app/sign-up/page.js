import "./sign-up.css"
// import { useNavigate } from 'react-router-dom'

export default function SignUp() {
  // const [username, setUsername] = useState('')
  // const [password, setPassword] = useState('')
  // const [error, setError] = useState('')
  // const [loading, setloading] = useState(false) 

  // const navigate = useNavigate()

  // const validateForm = () => {
  //   if (!username || !password){
  //     setError('Username and password are required')
  //     return false;
  //   }
  //   setError('')
  //   return true;
  // }

  // const handleSubmit = async (event) => {
  //   event.preventDefault();
  //   if (!validateForm()) return;
  //   setloading(true);

  //   const formDetails = new URLSearchParams();
  //   formDetails.append('username', username)
  //   formDetails.append('password', password)

  //   try{
  //     const response = await fetch('', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/x-www-form-urlencoded',
  //       },
  //       body: formDetails,
  //     });

  //     setloading(false);

  //     if (response.ok){
  //       const data = await response.json();
  //       localStorage.setItem('token', data.access_token)
  //       navigate('/protected');
  //     } else {
  //       const errorData = await response.json();
  //       setError(errorData.detail || 'Authentication failed!');
  //     }
  //   } catch(error){
  //     setloading(false);
  //     setError('An error occured. Please try again later.');
  //   }
  // }



  return (
    <>

    </>
  );
}   