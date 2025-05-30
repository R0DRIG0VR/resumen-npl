import  {Route, Routes} from 'react-router';
function App(){
    return(
        <Routes>
            <Route path="/" element={<h1>Home Page</h1>} />
        </Routes>
    )
}

export default App;