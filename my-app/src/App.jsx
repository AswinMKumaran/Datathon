import { useState } from 'react'
import './App.css'
import axios from "axios"
import { GoogleMap, useJsApiLoader, StandaloneSearchBox} from '@react-google-maps/api'
import {useRef} from 'react'
import Typewriter from 'typewriter-effect';



function App() {
  const inputref = useRef(null)
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: 'AIzaSyDUHsHCqoBgAQYFWrnACorleBAY8fV3D8I',
    libraries:["places"]
  })

  const [postYit, setPostYit] = useState(null)
  const [showVisibilityScore, setShowVisibilityScore] = useState(false);
  const [showMessage, setShowMessage] = useState("");
  const [showImage, setShowImage] = useState("");
  const [tshowImage, setTshowImage] = useState("");
  const [showScore, setShowScore] = useState(0.0);
  const [theAdd, setTheAdd] = useState("")

  const handlePostRequest = async () => {
    try {
      const dataToSend = { address: theAdd};

      const response = await axios.post("http://10.91.94.163:5001/image", dataToSend, {
        headers: { "Content-Type": "application/json" },
      });

      //const response = await axios.get("http://143.215.126.109:5001/");

      console.log("SUCCESS", response.data);
      setShowMessage(response.data["message"]);
      setShowScore(parseFloat(parseFloat(response.data["total_score"]).toFixed(2))+"/100");

       
      const image_URL = `data:image/jpeg;base64,${response.data["image_1"]}`;
      const timage_URL = `data:image/jpeg;base64,${response.data["image_2"]}`;
      setShowImage(image_URL);
      setTshowImage(timage_URL);
      setPostYit("Success: " + JSON.stringify(response.data));

      setShowVisibilityScore(true);

    } catch (error) {
      console.error("Error posting data:", error);
      setPostYit("Error: " + error.message);
    }
  };

  const handleOnPlacesChanged = () => {
    if (inputref.current) {
      const place = inputref.current.getPlaces()[0]; // Get first place result
  
      if (place) {
        const name = place.name; 
        const address = place.formatted_address; 
        
        const finalAddress = `${name}, ${address}`;
        setTheAdd(finalAddress)
        console.log("Final Address:", finalAddress);
      }
    }
  };
  const handleClick = () => {
    // Redirect to a new URL
    window.location.href = "https://anirudhkowlagi.github.io/HackGT/"; // Change this to the desired URL
  };
  const title = ['V I S I F Y',];
  
  return (
    <>
      <div style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh", 
      }}>
        
        <h1 className="typing-effect">
          <Typewriter
            onInit={(typewriter) => {
              // Loop through all but the last message
              title.slice(0, title.length - 1).forEach((message) => {
                typewriter
                  .typeString(message)
                  .pauseFor(1000)
                  .deleteAll(); // Deletes after each message
              });

              // Type the last message without deletion
              typewriter
                .typeString(title[title.length - 1])
                .pauseFor(1000) // Optional pause before finishing
                .start(); // Start the typing effect
            }}
          />
        </h1>

      
        
        <div style={{ display: "flex", alignItems: "center", paddingLeft: "10px" }}>
        
        {/* New button on the same line */}
        <button
          className="top-left-button"
          style={{ marginLeft: "5px", marginTop: "50px" }}
          onClick={handleClick} // Adding the redirect functionality here
        >
          Demo
      </button>
        </div>
        {showVisibilityScore &&(
          <div className="top-right-container">
          <h2>Impression Score</h2>
          <input type="text" className="top-right-input" defaultValue={showScore} />
          <textarea 
            className="top-right-textarea" 
            placeholder="Enter a sentence here..." 
            rows="4" 
            cols="30"
            defaultValue={showMessage}
            style={{ width: "100%", marginTop: "20px", padding: "8px", fontSize: "14px" }}
          />
          </div>
          
        )}
        


        
        <div style={{ marginTop: "5%", flexGrow: 1 }}>
          {isLoaded && (
            <StandaloneSearchBox
            onLoad={(ref) => (inputref.current = ref)}
            onPlacesChanged={handleOnPlacesChanged}
          >
            <div style={{ display: "flex", justifyContent: "center" }}>
              <input
                type="text"
                placeholder="Type in the address"
                className="input-field"
                style={{ width: "100%", maxWidth: "600px"}}
              />
            </div>
          </StandaloneSearchBox>
          )}

          {/* Post button under the input */}
          <button onClick={handlePostRequest} style={{ marginTop: "20px" }}>
            Find visibility
          </button>
          
          {showVisibilityScore && (
            <div style={{ display: "flex", alignItems: "center", justifyContent: "flex-start", marginTop: "100px" }}>

              <div
                style={{
                  position: "absolute",
                  top: "50%", // Adjust based on your preference
                  left: "27%",
                  transform: "translateX(-50%)",
                  color: "white", // Adjust title color
                  fontSize: "24px", // Adjust title font size
                  padding: "5px 10px", // Optional: add padding to title
                  borderRadius: "5px", // Optional: add border radius for a rounded title
                }}
              >
                <Typewriter
                  onInit={(typewriter) => {
                    typewriter
                      .typeString("Street View") // Type the title
                      .pauseFor(1000) // Optional pause before finishing
                      .start(); // Start the typing effect
                  }}
                />
              </div>
              <img
                src={showImage}
                alt="Description"
                style={{ width: "1000px", height: "auto", marginRight: "25px" }} // Adjust width and spacing as needed
              />
              <div
                style={{
                  position: "absolute",
                  top: "50%", // Adjust based on your preference
                  left: "72%",
                  transform: "translateX(-50%)",
                  color: "white", // Adjust title color
                  fontSize: "24px", // Adjust title font size
                  padding: "5px 10px", // Optional: add padding to title
                  borderRadius: "5px", // Optional: add border radius for a rounded title
                }}
              >
                <Typewriter
                  onInit={(typewriter) => {
                    typewriter
                      .typeString("YOLOv8") // Type the title
                      .pauseFor(1000) // Optional pause before finishing
                      .start(); // Start the typing effect
                  }}
                />
              </div>
              <img
                src={tshowImage}
                alt="Description"
                style={{ width: "1000px", height: "auto", marginLeft: "0px" }} // Adjust width and spacing as needed
              />
            </div>
          )}
        </div>

        

        {/* Content stays at the bottom */}
        
      </div>
    </>
  );
  
  
}

export default App
