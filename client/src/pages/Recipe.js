import React, { useState, useEffect } from 'react'
import "../style/main.css"
import axios from 'axios'
import { getCookie, snake_to_natural, natural_to_snake, snake_to_natural_2, natural_to_snake_2 } from '../utils/utils1'
import { HeartOutlined, HeartTwoTone, ShoppingTwoTone, ShoppingOutlined } from '@ant-design/icons';
// import { Icon } from "antd";

// export default function Recipe({ name, ingredients, time, calories, steps, macros, challengeRate}) {
export default function Recipe() {
	const [isLoading, setIsLoading] = useState(true)
	const [recipeId, setRecipeId] = useState("")
	const [recipe, setRecipe] = useState({})
	const [isHeart, setIsHeart] = useState(false)
	const [isShopingList, setIsShopingList] = useState(false)
	// const recipeData = {"name": "Moo Shu Beef Stir Fry", "ingredients": [{"name": "hoisin sauce","category": "condiments","quantity": "20","unit": "ml"},{"name": "sesame oil","category": "condiments","quantity": "3","unit": "ml"},{"name": "garlic clove","category": "vegetable","quantity": "0.25","unit": "-"},{"name": "ginger root","category": "vegetable","quantity": "1","unit": "g"},{"name": "rice vinegar","category": "conidments","quantity": "2.5","unit": "ml"},{"name": "asian chile paste","category": "condiments","quantity": "1.5","unit": "ml"},{"name": "lean sirloin steak, cut into strips","category": "meat","quantity": "120","unit": "g"},{"name": "cabbage slaw mix","category": "vegetable","quantity": "100","unit": "g"},{"name": "green onions","category": "vegetable","quantity": "1.5","unit": "-"},{"name": "cilantro","category": "vegetable","quantity": "1","unit": "g"}],"calories": "250","time_to_make": {"amount": "15","unit": "min"},"steps": "1) Whisk together the hoisin sauce, sesame oil, garlic, ginger, vinegar, and Asian chile paste in a bowl. 2) Season the beef with salt and pepper. 3) Heat a non-stick skillet over high heat. Once hot, spray with cooking spray and add the beef. Cook for 3-4 minutes until done to your liking. 4) Remove the beef and set aside. Add more cooking spray and add the scallions, cabbage, and sauce. Cook for about 5 minutes until the cabbage is cooked. 5) Turn off the heat and stir in the beef. Top with cilantro.","macros": [{"name": "Protein","amount": "27","unit": "g"},{"name": "Fat","amount": "7","unit": "g"},{"name": "Carbs","amount": "18","unit": "g"}],"challenge_rate": 2,"tag": []}

	const loadData = async (id) => {
		const resp = await axios.get("https://cloud-cw-team-server-upikjd2l6a-ew.a.run.app/api/getRecipe?name=" + id)
		console.log("recipe")
		console.log(resp.data.recipe)
		setRecipe(resp.data.recipe)
	}

	useEffect(() => {
		const splitted = window.location.href.split("/")
		const rid = splitted[splitted.length - 1]
		setRecipeId(rid)
		loadData(rid)
		setIsLoading(false)
	}, [])

	return ((isLoading) ? <span>Loading. Please refresh the page if the loading takes too long.</span> :
	(
		<>
			<section style={{ "display": "flex", alignItems: "center", justifyContent: "center", flexDirection: "column" }}>
				<div className="section-1" style={{ height: "35vh" }}>
					<div style={{ "margin-right": "20px" }}>
						<img style={{ height: '100%', width: '100%', maxHeight: "200px" }} src={recipe.image} alt=""/>
					</div>
					<div>
						<h2>{(recipe.name) && snake_to_natural_2(recipe.name)}</h2>
						<span>{(recipe.difficulty) && "🏋️" + recipe.difficulty}</span>
						<span>{(recipe.time_to_make) && "⏰" + recipe.time_to_make.amount + " " + recipe.time_to_make.unit}</span>
						<span>{(recipe.price) && "🤑" + recipe.price.amount + " " + recipe.price.unit}</span>
					</div>
				</div>
			</section>

			<section style={{ "display": "flex", alignItems: "flex-start", marginLeft: "22vw", marginTop: "15px" }}>
				<div style={{ "display": "flex", "flexDirection": "row", justifyContent: "space-between", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", "border-radius": "5px", width: "52vw" }}>
					<div style={{paddingLeft: "20px"}}>
						<h3>Ingredients</h3>
						<ul>
						{ recipe.ingredients && recipe.ingredients.map(e => <li>{e.name + ": " + e.quantity + e.unit}</li>) }
						</ul>
					</div>
					<div style={{paddingRight: "20px"}}>
						<h3>Steps</h3>
						<ul>
						{recipe.steps && (
							<section>
							{recipe.steps.map((step, index) => (
								<div key={step.key}>
								<h2 >{step.name}</h2>
								<p style= {{ display: "inline-block", width: "20vw" }}>{step.content}</p>
								</div>
							))}
							</section>
						)}
						</ul>
					</div>
				</div>
			</section>

			<section style={{ display: "flex", alignItems: "center", justifyContent: "center", marginTop: "20px" }}>
				<div style={{ "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", "border-radius": "5px", width: "52vw", marginRight: "20px"}}>
					{recipe.macros && (
					<ul className="recipe__macros">
					{recipe.macros.map((macro, index) => (
						<li key={index} className="recipe__ingredient">
						<span className="recipe__macro-name">{macro.name}:</span> {macro.amount} {macro.unit}
						</li>
					))}
					</ul>
					)}
			  </div>
		  </section>
		</>
	))
}
const ClickableIcon = (props) => (
	<a onClick={() => {props.func(!props.value)}} style={{ cursor: "pointer", marginLeft: "8px" }}>
		{(props.value) ? <props.icon1 style={{ fontSize: '150%'}}/> : <props.icon2 style={{ fontSize: '150%'}}/>}
	</a>)