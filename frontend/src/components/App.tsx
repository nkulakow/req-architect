import {useEffect, useState} from "react";

function App() {
    const [text, setText] = useState('')
    useEffect(() => {
        fetch(import.meta.env.VITE_APP_API_URL + '/demoapp/hello').then(res => res.text()).then(setText)
    }, []);
    return (
    <p>
        {text}
    </p>
  )
}

export default App
