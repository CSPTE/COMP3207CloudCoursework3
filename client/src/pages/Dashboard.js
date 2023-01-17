import React, { useEffect, useState } from 'react'
import { useNavigate } from "react-router-dom";
import { getCookie, snake_to_natural, natural_to_snake, natural_to_snake_2, snake_to_natural_2 } from "../utils/utils1"
import Recipe from './Recipe';
import axios from "axios";
import { Col, Divider, Row } from 'antd';
import { Space, Table, Modal, Button, Tabs } from 'antd';

export default function Dashboard() {
	const [isLoading, setIsLoading] = useState(true)
	const [user, setUser] = useState({})
	const [recipes, setRecipes] = useState({})
	const [recipesToAdd, setRecipesToAdd] = useState({})
	const [recipesToAddFavorites, setRecipesToAddFavorites] = useState({})
	const [isOpen, setIsOpen] = useState(false)
	const [keyToUpdate, setKeyToUpdate] = useState(0)

	const today = new Date();
	const day = today.getDate();
	const month = today.toLocaleString('default', { month: 'long' });


	const loadData = async () => {
		console.log(getCookie("_auth_state"))
		let user_tmp = await JSON.parse(getCookie("_auth_state"))
		console.log(user_tmp)
		const resp = await axios.post("https://izifood.azurewebsites.net/api/addToShoppingList?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: user_tmp.email, action: "getAll" }, { 'Content-Type': 'application/json'} )
		const resp_favorites = await axios.post("https://izifood.azurewebsites.net/api/updateFavorite?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: user_tmp.email, action: "getAll" }, { 'Content-Type': 'application/json'} )
		const resp_2 = await axios.get("https://izifood.azurewebsites.net/api/getRecipes?action=getAll")
		if (resp_2.data.status == "error") {
			console.log(resp_2.data.message)
			return
		}
		let dataToAdd = []
		let dataToAddFavorites = []
		console.log(resp_2.data.recipes)
		for (let i in resp_2.data.recipes) {
			console.log("i: ", i)
			dataToAdd.push({ "key": i + 1,"recipe-name": resp_2.data.recipes[i].name,"price": resp_2.data.recipes[i].price.amount,"health": "5" })
		}
		for (let i in resp_favorites.data.data) {
			console.log("i: ", i)
			dataToAddFavorites.push({ "key": i + 1,"recipe-name": resp_favorites.data.data[i].name,"price": resp_favorites.data.data[i].price.amount,"health": "5" })
		}
		setRecipesToAdd(dataToAdd)
		setRecipesToAddFavorites(dataToAddFavorites)
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
		<h1>Dashboard</h1>
		<section>
			<div style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>

				<div style={{ display: "flex", marginRight: "30px", flexDirection: "column", alignItems: "center", justifyContent: "center", width: "180px", height: "180px", backgroundColor: "rgb(238, 238, 238)" ,"box-shadow": "0 2px 4px rgba(0, 0, 0, 0.1)", "border-radius": "5px" }}>
					<span>{month}</span>
					<span>{day}</span>
				</div>

				<div style={{ display: "flex", flexDirection: "column", width: "360px", height: "180px", backgroundColor: "rgb(238, 238, 238)" ,"box-shadow": "0 2px 4px rgba(0, 0, 0, 0.1)", "border-radius": "5px" }}>
					<div style={{ padding: "10px" }}>
						<span>Today's recipe</span>
						{/* render image + name + emojis related to recipe (time, effort...) */}
					</div>
				</div>

			</div>
		</section>

		<section>
			<h2>Recipes of the week</h2>
			<div style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
				<Table columns={columns} dataSource={recipes} /> {/* Reverse table? with days as field name? */}
			</div>
		</section>

		<Modal title="Basic Modal" open={isOpen} onCancel={cancelModal} onOk={okModal}>
		<Tabs className="tabs"
			items={[
				{ label: 'Favorites <3', key: '1', children: <Table columns={columnsModal} dataSource={recipesToAddFavorites} pagination={{ pageSize: 5 }}/>},
				{ label: 'All', key: '2', children: <Table columns={columnsModal} dataSource={recipesToAdd} pagination={{ pageSize: 5 }}/>}]}
		/>
		</Modal>
		</>
	)
}
