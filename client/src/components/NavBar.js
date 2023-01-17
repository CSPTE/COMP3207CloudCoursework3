import React, { useState } from 'react'
import { AppstoreOutlined, DashboardOutlined, SettingOutlined, ShoppingCartOutlined } from '@ant-design/icons';
import { Menu } from 'antd';
import { Button, Form, Input, Typography } from 'antd';
import { useSignOut } from "react-auth-kit";
import { useNavigate } from "react-router-dom";
import { getCookie } from "../utils/utils1";
import mainLogo from "../IzzyFoodNoBg.png"
import "../style/main.css"

export default function NavBar() {
	const [current, setCurrent] = useState("profile");
	const singOut = useSignOut()
	const navigate = useNavigate()
	const items = [
		{
			label: <a href="/dashboard">Dashboard</a>,
			key: 'dashboard',
			icon: <DashboardOutlined />,
			show: true,
		},
		{
			label: 'Recipes',
			key: 'recipes',
			icon: <AppstoreOutlined />,
			show: true,
			children: [
				{
					label: <a href="/browse-recipes" block>Browse Recipes</a>,
					key: "browse-recipes"
				},
				{
					label: <a href="/favorite-recipes" block>Favorite Recipes</a>,
					key: "favorite-recipes"
				},
				{
					label: <a href="/recipes-of-the-week" block>Recipes of the week</a>,
					key: "recipes-of-the-week"
				},
			]
		},
		{
			label: 'Ingredients',
			key: 'ingredients',
			icon: <ShoppingCartOutlined />,
			show: true,
			children: [
				{
					label: <a href="/shopping-list" block>Shopping List</a>,
					key: "shopping-list"
				},
				{
					label: <a href="/my-fridge" block>My Fridge</a>,
					key: "my-fridge"
				},
			]
		},
		{
			label: <a href="/profile">Profile</a>,
			key: 'profile',
			icon: <SettingOutlined />,
			show: true,
		},
		{
			label: (<Button onClick={() => {singOut(); navigate("/login")}} block>Log out</Button>),
			key: "logout",
			show: true,
		}
	]


	const onClick = (e) => {
		console.log('click ', e);
		document.cookie = "tabKey=" + e.key;
		setCurrent(e.key);
	};

	return (
		<div className="center-div">
			<img src={mainLogo} alt="" style={{width: "150px"}} />
			<Menu style={{width: "45vw"}} onClick={onClick} selectedKeys={[getCookie("tabKey")]} mode="horizontal" items={items} />
		</div>
		)
}
