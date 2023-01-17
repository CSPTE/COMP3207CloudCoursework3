import React, { useEffect, useState } from 'react'
import { useNavigate } from "react-router-dom";
import { getCookie, snake_to_natural, natural_to_snake, snake_to_natural_2, natural_to_snake_2 } from "../utils/utils1"
import Recipe from './Recipe';
import axios from "axios";
import { Col, Divider, Row } from 'antd';
import { HeartOutlined, HeartTwoTone, ShoppingTwoTone, ShoppingOutlined } from '@ant-design/icons';
const recipeData = {"name": "Moo Shu Beef Stir Fry", "ingredients": [{"name": "hoisin sauce","category": "condiments","quantity": "20","unit": "ml"},{"name": "sesame oil","category": "condiments","quantity": "3","unit": "ml"},{"name": "garlic clove","category": "vegetable","quantity": "0.25","unit": "-"},{"name": "ginger root","category": "vegetable","quantity": "1","unit": "g"},{"name": "rice vinegar","category": "conidments","quantity": "2.5","unit": "ml"},{"name": "asian chile paste","category": "condiments","quantity": "1.5","unit": "ml"},{"name": "lean sirloin steak, cut into strips","category": "meat","quantity": "120","unit": "g"},{"name": "cabbage slaw mix","category": "vegetable","quantity": "100","unit": "g"},{"name": "green onions","category": "vegetable","quantity": "1.5","unit": "-"},{"name": "cilantro","category": "vegetable","quantity": "1","unit": "g"}],"calories": "250","time_to_make": {"amount": "15","unit": "min"},"steps": "1) Whisk together the hoisin sauce, sesame oil, garlic, ginger, vinegar, and Asian chile paste in a bowl. 2) Season the beef with salt and pepper. 3) Heat a non-stick skillet over high heat. Once hot, spray with cooking spray and add the beef. Cook for 3-4 minutes until done to your liking. 4) Remove the beef and set aside. Add more cooking spray and add the scallions, cabbage, and sauce. Cook for about 5 minutes until the cabbage is cooked. 5) Turn off the heat and stir in the beef. Top with cilantro.","macros": [{"name": "Protein","amount": "27","unit": "g"},{"name": "Fat","amount": "7","unit": "g"},{"name": "Carbs","amount": "18","unit": "g"}],"challenge_rate": 2,"tag": []}


export default function BrowseRecipes() {
	const [isLoading, setIsLoading] = useState(true)
	const [user, setUser] = useState({})
	const [recipes, setRecipes] = useState([])
	const [isHeart, setIsHeart] = useState(false)
	const [isShopingList, setIsShopingList] = useState(false)

	const getRecipes = async (email) => {
		const resp = await axios.get("https://izifood.azurewebsites.net/api/getRecipes?action=getAll")
		if (resp.data.status == "error") {
			console.log(resp.data.message)
			return
		}
		console.log("data received")
		console.log(resp.data.recipes)
		await getFavorites(resp.data.recipes)
	}

	const getFavorites = async (recep) => {
		let tmp = JSON.parse(getCookie("_auth_state"))
		const resp = await axios.post("https://izifood.azurewebsites.net/api/updateFavorite?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: tmp.email, action: "getAllAsString" })
		if (resp.data.result == "error") {
			console.log(resp.data)
			return
		}
		const favorites = resp.data.data

		let recipesTmp = [...recep]
		recipesTmp.forEach((e, k) => e.isFavorite = (favorites.indexOf(natural_to_snake_2(e.name)) > -1) ? true : false )
		setRecipes(recipesTmp)
	}

	const addToShoppingList = (recipe, ext) => {
		let recipesTmp = [...recipes]
		recipesTmp.forEach(async (e) => {
			if (e.name == recipe.name) {
				if ((ext == "updateFavorite") ? !e.isFavorite : !e.isShoppingList) {
					const resp = await axios.post("https://izifood.azurewebsites.net/api/" + ext + "?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: user.email, action: "add", recipeName: natural_to_snake_2(e.name) })
					if (resp.data.result == "error") {
						alert("error try later")
						return
					}			
				} else {
					const resp = await axios.post("https://izifood.azurewebsites.net/api/" + ext + "?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: user.email, action: "remove", recipeName: natural_to_snake_2(e.name) })
					if (resp.data.result == "error") {
						alert("error try later")
						return
					}			
				}
				if (ext == "updateFavorite")
					e.isFavorite = !e.isFavorite
				else
					e.isShoppingList = !e.isShoppingList
				
				setRecipes(recipesTmp)
				return
			}
		})
	}

	useEffect(() => {
		try {
			let user_tmp = JSON.parse(getCookie("_auth_state"))
			console.log(user_tmp)
			setUser(user_tmp)
			getRecipes(user_tmp.email)
			setIsLoading(false)
		} catch (e) {
			console.log(e)
		}
	}, [])

	return (isLoading) ?  (<span>Loading. Please refresh the page if the loading takes too long.</span>) :
	(
		<div >
			{/* <Row style={{ "display": "flex", alignItems: "center", alignContent: "center" }}> */}
			<div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
				<div style={{ display: 'flex', flexWrap: 'wrap', width: '90%' }}>
			{
			  recipes.map((e, k) => {
					let link = "/recipe/" + natural_to_snake(e.name)
					return (
						<>
						<div style={{ "box-shadow": "0 2px 4px rgba(0, 0, 0, 0.1)", margin: "10px", padding: "8px", "border-radius": "5px", width: '30%', height: 'auto' }}>
						<div >
								<h3>{snake_to_natural_2(e.name)}</h3>
								<span>{(e.difficulty) && "🏋️ " + e.difficulty}</span>
								<span>{(e.time_to_make) && "⏰ " + e.time_to_make.amount + " " + e.time_to_make.unit}</span>
								<span>{(e.price) && "🤑 " + e.price.amount + " " + e.price.unit}</span>

								<div style={{ display: "flex", justifyContent: "flex-end", alignItems: "center" }}>
									Add To favorites
									<a onClick={() => addToShoppingList(recipes[k], "updateFavorite")} style={{ cursor: "pointer", marginLeft: "8px" }}>
										{((recipes[k])?.isFavorite) ? <HeartTwoTone style={{ fontSize: '150%'}}/> : <HeartOutlined style={{ fontSize: '150%'}}/>}
									</a>
									{/* <a onClick={() => addToShoppingList(recipes[k], "addToShoppingList")} style={{ cursor: "pointer", marginLeft: "8px" }}>
										{((recipes[k])?.isShoppingList) ? <ShoppingTwoTone style={{ fontSize: '150%'}}/> : <ShoppingOutlined style={{ fontSize: '150%'}}/>}
									</a> */}
								</div>
								<a href={link}><img src={e.image} alt="" style={{ height: '100%', width: '100%', maxHeight: "200px" }}/></a>
							</div>
						</div>
						</>
					)
				})
			}
				</div>
			</div>
		</div>
	)
}

const ClickableIcon = (props) => (
	<a onClick={() => {props.func(!props.value)}} style={{ cursor: "pointer", marginLeft: "8px" }}>
		{(props.value) ? <props.icon1 style={{ fontSize: '150%'}}/> : <props.icon2 style={{ fontSize: '150%'}}/>}
	</a>
)
