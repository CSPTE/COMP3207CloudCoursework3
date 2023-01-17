import React, { useEffect, useState } from "react"
import {
	BrowserRouter as Router,
	Route,
	Routes,
	Navigate
} from "react-router-dom"

import Signup from "./pages/Signup"
import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard";
import BrowseRecipes from "./pages/BrowseRecipes";
import FavoriteRecipes from "./pages/FavoriteRecipes";
import RecipesOfTheWeek from "./pages/RecipesOfTheWeek";
import Profile from "./pages/Profile";
import ShoppingList from "./pages/ShoppingList";
import MyFridge from "./pages/MyFridge";
import NavBar from "./components/NavBar";
import { RequireAuth } from "react-auth-kit";
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from "react-auth-kit";
import Recipe from "./pages/Recipe";

function App() {
	// const [isLoggedIn, setIsLoggedIn] = useState(false)
	// // let isLoggedIn = localStorage.getItem("email") != "";

	// useEffect(() => {
	// 	console.log(localStorage.getItem("email") != "")
	// 	setIsLoggedIn(localStorage.getItem("email") != "")
	// }, [isLoggedIn])
	console.log("4")

	return (
		<AuthProvider
		authType={"cookie"}
		authName={"_auth"}
		cookieDomain={window.location.hostname}
		cookieSecure={false}>
		<BrowserRouter>

		<Routes>
			<Route path="/login" element={<Login />} />
			<Route path="/signup" element={<Signup />} />
			<Route path="*" element={<RequireAuth loginPath="/login"> <MainPages /> </RequireAuth> } />

			{/* <Route path="*" element={isLoggedIn ? <MainPages /> : <Navigate to='/login' replace />} /> */}
		</Routes>
		</BrowserRouter>
		</AuthProvider>
	);
}

const MainPages = () => (
	<>
		<nav>
			<NavBar/>
		</nav>
		<Routes>
		<Route path="/dashboard" element={ <RequireAuth loginPath="/login"><Dashboard /></RequireAuth> } />
		{/* <Route path="/dashboard" element={<Dashboard /> } /> */}

		<Route path="/recipe/:recipe_id" element={<Recipe />} />
		<Route path="/browse-recipes" element={<BrowseRecipes />} />
		<Route path="/favorite-recipes" element={<FavoriteRecipes />} />
		<Route path="/favorite-recipes" element={<FavoriteRecipes />} />

		<Route path="/recipes-of-the-week" element={<RecipesOfTheWeek />} />
		<Route path="/profile" element={<Profile />} />
		<Route path="/shopping-list" element={<ShoppingList />} />
		<Route path="/my-fridge" element={<MyFridge />} />
		</Routes>
	</>
)

export default App;
