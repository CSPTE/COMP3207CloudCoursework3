import React, { useEffect, useState } from "react"
import FridgeItem from "../components/FridgeItem";
import { getCookie, snake_to_natural, natural_to_snake, snake_to_natural_2, natural_to_snake_2 } from "../utils/utils1"
import { Form, Input, Select, Table, Modal, Button, Tabs } from "antd";
import axios from "axios";
import { ConsoleSqlOutlined } from "@ant-design/icons";

const units = ["-", "g", "ml"]

const removeItem = async (record, setItems, items) => {
	let newItems = items.filter(e => e.name != record.name)
	let tmp = JSON.parse(getCookie("_auth_state"))
	const resp = await axios.post("https://izifood.azurewebsites.net/api/removeFromFridge?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: tmp.email, ingredient: record })
	if (resp.data.result == "error") {
		alert(resp.data.msg)
		return
	}

	setItems(newItems)
	return true
}

export default function MyFridge() {
	//Put Javascript here
	const [isLoading, setIsLoading] = useState(true)
	const [items, setItems] = useState([]);
	const [isPopupOpen, setIsPopupOpen] = useState(false);
  	const [newIngredient, setNewIngredient] = useState("");
  	const [newAmount, setNewAmount] = useState("");
  	const [newUnit, setNewUnit] = useState("");
  	const [allIngredients, setAllIngredients] = useState([]);
	const { Option } = Select


	const columns = [
		{ title: "Ingredient",dataIndex: "name",key: "name" },
		{ title: "Amount",dataIndex: "quantity",key: "quantity" },
		{ title: "unit",dataIndex: "unit", key: "unit" },
		{ title: "Remove",dataIndex: "remove",key: "remove",render: (_, record) => <Button onClick={() => { removeItem(record, setItems, items) }} type="primary">Remove</Button> },
	]


	const loadData = async () => {
		let tmp = JSON.parse(getCookie("_auth_state"))
		const resp = await axios.post("https://izifood.azurewebsites.net/api/getIngredients?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: tmp.email })
		if (resp.data.result == "error") {
			alert(resp.data.msg)
			return
		}

		const resp_fridge = await axios.post("https://izifood.azurewebsites.net/api/getFridge?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: tmp.email })
		if (resp_fridge.data.result == "error") {
			alert(resp_fridge.data.msg)
			return
		}
		setItems(resp_fridge.data.data)

		setAllIngredients(resp.data.data)
		setIsLoading(false)
	}
	
    function toAddIngredient() {
		setIsPopupOpen(true);
    }
	
	async function addIngredientToFridge() {
		let tmp = JSON.parse(getCookie("_auth_state"))
		const resp = await axios.post("https://izifood.azurewebsites.net/api/addtofridge?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: tmp.email, ingredient: {  name: newIngredient, quantity: newAmount, unit: newUnit } })
		if (resp.data.result == "error") {
			alert(resp.data.msg)
			return
		}
		setItems([...items, { key: items.length + 1, name: newIngredient, quantity: newAmount, unit: newUnit }]);
		setNewIngredient("")
		setNewAmount("")
		setNewUnit("")
		setIsPopupOpen(false);
	}

	const cancelModal = () => {
		setIsPopupOpen(false)
	}

	useEffect(() => {
		loadData()
	}, [])

	/**
	 * TODO: Should be able to query a list of ingredients -> much easier for price
	 * Connect add / remove with db
	 */
	return (isLoading) ? <span>Loading. Please refresh the page if the loading takes too long.</span> : (
		<>
		<h1>My Fridge</h1>
		<section>
			<div style={{ display: "flex", alignItems: "flex-end", justifyContent: "flex-end", marginRight: "10vw", marginBottom: "15px" }}>
				<Button onClick={toAddIngredient}>Add Ingredient</Button>
			</div>
			<div style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
			<div style={{ width: "80%" }}>
				<Table columns={columns} dataSource={items}></Table>
			</div>
			</div>
		</section>
		<Modal open={isPopupOpen} onCancel={cancelModal} onOk={addIngredientToFridge}>
			<Form style={{ padding: "20px" }}>
				<h3>Search ingredient</h3>
				<Select showSearch onSelect={(e) => {
					let ingredient = allIngredients.filter(elem => elem.name == e)[0]
					setNewIngredient(ingredient.name)
					setNewAmount(ingredient.quantity)
					setNewUnit(ingredient.unit)
					// setItems([...items, { key: items.length + 1, name: ingredient.name, quantity: ingredient.quantity, unit: ingredient.unit }]);
				}} style={{ width: "100%" }} placeholder="Search ingredient">
					{ allIngredients.map(e => <Option value={e.name}>{e.name}</Option>) }
				</Select>
				<h3>Add ingredient</h3>
				<Input style={{ marginBottom: "10px" }} placeholder="Ingredient name" onChange={(e) => setNewIngredient(e.target.value)} value={newIngredient} />
				<div style={{ display: "flex", marginTop: "10px" }}>
					<Input style={{ width: "50%" }} placeholder="Amount" onChange={(e) => setNewAmount(e.target.value)} value={newAmount}/>
					<Select showSearch value={newUnit} onSelect={(e) => setNewUnit(e)} style={{ width: "150%" }} placeholder="Unit">
						{ units.map(e => <Option value={e}>{e}</Option>) }
					</Select>
				</div>
			</Form>
		</Modal>
		</>
		);
}