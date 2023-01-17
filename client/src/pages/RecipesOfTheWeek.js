import React, { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom";
import { getCookie, snake_to_natural, natural_to_snake, natural_to_snake_2, snake_to_natural_2 } from "../utils/utils1"
import Recipe from "./Recipe";
import axios from "axios";
import { Col, Divider, Row } from "antd";
import { Space, Table, Modal, Button } from "antd";

export default function RecipesOfTheWeek() {
	const [isLoading, setIsLoading] = useState(true)
	const [user, setUser] = useState({})
	const [recipes, setRecipes] = useState({})
	const [recipesToAdd, setRecipesToAdd] = useState({})
	const [isOpen, setIsOpen] = useState(false)
	const [keyToUpdate, setKeyToUpdate] = useState(0)
	const nav = useNavigate()

	const loadData = async () => {
		let user_tmp = JSON.parse(getCookie("_auth_state"))
		const resp = await axios.post("https://izifood.azurewebsites.net/api/addToShoppingList?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: user_tmp.email, action: "getAll" } )
		const resp_2 = await axios.get("https://cloud-cw-team-server-upikjd2l6a-ew.a.run.app/api/getAllRecipes?email=" + user_tmp.email)
		if (resp_2.data.status == "error") {
			console.log(resp_2.data.message)
			return
		}
		let dataToAdd = []
		console.log(resp_2.data.recipes)
		for (let i in resp_2.data.recipes) {
			console.log("i: ", i)
			dataToAdd.push({ "key": i + 1,"recipe-name": resp_2.data.recipes[i].name,"price": resp_2.data.recipes[i].price.amount,"health": "5" })
		}
		console.log(dataToAdd)
		setRecipesToAdd(dataToAdd)
		console.log("data received")
		setRecipes(resp.data.data)
		setIsLoading(false)
	}

	// TODO: add changes to the database
	const removeRecipe = async (toRemove) => {
		let recipesTmp = [...recipes]

		toRemove = recipesTmp.filter(e => e["key"] == toRemove["key"])[0]
		recipesTmp = recipesTmp.filter(e => e["key"] != toRemove["key"])
		Object.assign(toRemove, {"recipe-name": "", "price": "", "health": ""})
		recipesTmp.push(toRemove)
		recipesTmp = recipesTmp.sort((a,b) => a.key - b.key)
		let user_tmp = JSON.parse(getCookie("_auth_state"))
		await axios.post("https://izifood.azurewebsites.net/api/addToShoppingList?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: user_tmp.email, toPush: recipesTmp, action: "update" })
		setRecipes(recipesTmp)
	}

	const addRecipe = async (record) => {
		setIsOpen(true)
		setKeyToUpdate(record.key)

	}
	const addRecipeFromModal = async (record) => {
		let recipesTmp = [...recipes]
		let toPush = {}

		toPush = recipesTmp.filter(e => e["key"] == keyToUpdate)[0]
		recipesTmp = recipesTmp.filter(e => e["key"] != keyToUpdate)
		Object.assign(toPush, {"recipe-name": record["recipe-name"], "price": record.price, "health": record.health})
		recipesTmp.push(toPush)
		recipesTmp = recipesTmp.sort((a,b) => a.key - b.key)
		
		let user_tmp = JSON.parse(getCookie("_auth_state"))
		await axios.post("https://izifood.azurewebsites.net/api/addToShoppingList?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: user_tmp.email, toPush: recipesTmp, action: "update" })
		setRecipes(recipesTmp)
		setIsOpen(false)
	}

	const columns = [
		{ title: "Day",dataIndex: "day",key: "day" },
		{ title: "Recipe Name",dataIndex: "recipe-name",key: "recipe-name",render: (txt) => (<><a href={"/recipe/" + natural_to_snake_2(txt)}>{txt}</a></>) },
		{ title: "Price",dataIndex: "price",key: "price", render: (txt) => <span>£{txt}</span> },
		{ title: "Health score",dataIndex: "health",key: "health",render: (txt) => <span>{txt}/5</span> },
		{
			title: "Action",
			dataIndex: "action",
			key: "action",
			render: (_, record) => (
				<Space>
					<a onClick={() => addRecipe(record)}>Add</a>
					<a onClick={(e) => {removeRecipe(record)}}>Remove</a>
				</Space>
			)
		}
	];

	const columnsModal = [
		{ title: "Recipe Name",dataIndex: "recipe-name",key: "recipe-name",render: (txt) => (<><a href={"/recipe/" + natural_to_snake_2(txt)}>{txt}</a></>) },
		{ title: "Price",dataIndex: "price",key: "price", render: (txt) => <span>£{txt}</span> },
		{ title: "Health score",dataIndex: "health",key: "health",render: (txt) => <span>{txt}/5</span> },
		{
			title: "Add",
			dataIndex: "add",
			key: "add",
			render: (_, record) => (
				<Button onClick={() => addRecipeFromModal(record)}>Add</Button>
			)
		}
	];

	const clearRecipes = async () => {
		let user_tmp = JSON.parse(getCookie("_auth_state"))
		const resp = await axios.post("https://izifood.azurewebsites.net/api/addToShoppingList?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: user_tmp.email, action: "clear" })
		setRecipes(resp.data.data)
	}

	const generateRecipes = async () => {
		let toPush = []
		for (let i in recipes)
			if (recipes[i]["recipe-name"] != "")
				toPush.push(recipes[i]["recipe-name"])
		console.log(toPush)
		let user_tmp = JSON.parse(getCookie("_auth_state"))
		const resp = await axios.post("https://izifood.azurewebsites.net/api/ShoppingListIngredient?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: user_tmp.email, recipes: toPush })
		console.log(resp.data.data)
		nav("/shopping-list")
	}

	const cancelModal = () => {
		setIsOpen(false)
	}

	const okModal = () => {
		setIsOpen(false)
	}

	useEffect(() => {
		loadData()
	}, [])

	return (isLoading) ?  (<span>Loading. Please refresh the page if the loading takes too long.</span>) :
	(
		<>
		<h1>RecipesOfTheWeek</h1>
		<div style={{ display: "flex", alignItems: "center", justifyContent: "center", }}>
		<div style={{ "box-shadow": "4px rgba(0, 0, 0, 0.1)", width: "70%" }}>
			<div style={{ display: "flex", alignItems: "center", justifyContent: "flex-end", marginBottom: "12px", marginRight: "3vw" }}>
				<Button type="primary" style={{ marginRight: "8px" }} onClick={generateRecipes}>Generate shopping list</Button>
				<Button onClick={clearRecipes}>Clear all</Button>
			</div>
			<section>
				<div style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
					<Table columns={columns} dataSource={recipes} /> {/* Reverse table? with days as field name? */}
				</div>
			</section>
		</div>
		</div>

		<Modal title="Basic Modal" open={isOpen} onCancel={cancelModal} onOk={okModal}>
			<Table columns={columnsModal} dataSource={recipesToAdd} pagination={{ pageSize: 5 }}/> {/* Reverse table? with days as field name? */}
		</Modal>
		</>
	)
}
