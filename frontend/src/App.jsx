import Intro from "./components/Profile/Intro";
import StaticBackground from "./components/Layout/Background.jsx";
import ChatWidget from "./components/Chat/ChatWidget";
import "./index.css";
import "./App.css";

function App() {
    return (
        <>
            <StaticBackground/>
            <Intro/>
            <ChatWidget/>
        </>
    );
}

export default App;
