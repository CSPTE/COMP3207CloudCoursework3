import React, { useEffect, useState } from "react"
import FridgeItem from "../components/FridgeItem";
import { getCookie, snake_to_natural, natural_to_snake, snake_to_natural_2, natural_to_snake_2 } from "../utils/utils1"
import { Form, Input, Select, Table, Modal, Button, Tabs } from "antd";
import axios from "axios";

const units = ["-", "g", "ml"]

const removeItem = async (record, setItems, items) => {
	let newItems = items.filter(e => e.name != record.name)
	let tmp = JSON.parse(getCookie("_auth_state"))
	const resp = await axios.post("https://izifood.azurewebsites.net/api/UpdateToShoppingListIngredients?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: tmp.email, action: "remove", item: record })
	if (resp.data.result == "error") {
		alert(resp.data.msg)
		return
	}

	setItems(newItems)
	return true
}

const getTotal = (data) => {
	let total = 0
	for (let i in data)
		total += parseFloat(data[i].price)
	return total
}

export default function ShoppingList() {
	//Put Javascript here
	const [isLoading, setIsLoading] = useState(true)
	const [items, setItems] = useState([]);
	const [isPopupOpen, setIsPopupOpen] = useState(false);
	const [newIngredient, setNewIngredient] = useState("");
	const [newAmount, setNewAmount] = useState("");
	const [newUnit, setNewUnit] = useState("");
	const [newPrice, setNewPrice] = useState(0);

	const [allIngredients, setAllIngredients] = useState([]);
	const { Option } = Select

	const columns = [
		{ title: "Ingredient",dataIndex: "name",key: "name" },
		{ title: "Amount",dataIndex: "quantity",key: "quantity" },
		{ title: "unit",dataIndex: "unit", key: "unit" },
		{ title: "Price (£)",dataIndex: "price", key: "price" },		
		{ title: "Remove",dataIndex: "remove",key: "remove",render: (_, record) => <Button onClick={() => { removeItem(record, setItems, items) }} type="primary">Remove</Button> },
	]

	const loadData = async () => {
		let tmp = JSON.parse(getCookie("_auth_state"))
		const resp = await axios.post("https://izifood.azurewebsites.net/api/getIngredients?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: tmp.email })
		if (resp.data.result == "error") {
			alert(resp.data.msg)
			return
		}

		const resp_fridge = await axios.post("https://izifood.azurewebsites.net/api/UpdateToShoppingListIngredients?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: tmp.email, action: "getAll" })
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
		const numberRegex = /[+-]?([0-9]*[.])?[0-9]+/;
		const stringAndNumberRegex = /^[a-zA-Z0-9 ]*$/;
		const stringRegex = /^[a-zA-Z ]*$/;
		if (!stringRegex.test(newIngredient)) {
			alert("Ingredient Name must be a string of characters");
			return ;
		}
		if (!stringAndNumberRegex.test(newAmount)) {
			alert("Ingredient Amount must be a string that contains letters and numbers");
			return ;
		}
		if (!numberRegex.test(newPrice)) {
			alert("Ingredient Price must be a number");
			return ;
		}

		let tmp = JSON.parse(getCookie("_auth_state"))
		const resp = await axios.post("https://izifood.azurewebsites.net/api/UpdateToShoppingListIngredients?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: tmp.email, action: "add", item: {  name: newIngredient, quantity: newAmount, unit: newUnit, price: newPrice } })
		if (resp.data.result == "error") {
			alert(resp.data.msg)
			return
		}
		setItems([...items, { key: items.length + 1, name: newIngredient, quantity: newAmount, unit: newUnit, price: newPrice }]);
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
		<h1>Shopping list</h1>
		<section>
			<div style={{ display: "flex", alignItems: "flex-end", justifyContent: "flex-end", marginRight: "10vw", marginBottom: "15px" }}>
			<Button onClick={toAddIngredient}>Add Ingredient</Button>
			</div>
			<div style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
			<div style={{ width: "80%" }}>
				<Table footer={()=>"Total price: " + getTotal(items)} columns={columns} dataSource={items}></Table>
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
					setNewPrice(ingredient.price)
				}} style={{ width: "100%" }} placeholder="Search ingredient">
					{ allIngredients.map(e => <Option value={e.name}>{e.name}</Option>) }
				</Select>
				<h3>Add ingredient</h3>
				<Input style={{ marginBottom: "10px" }} placeholder="Ingredient name" onChange={(e) => setNewIngredient(e.target.value)} value={newIngredient} />
				<Input placeholder="Price" onChange={(e) => setNewPrice(e.target.value)} value={newPrice} />
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
