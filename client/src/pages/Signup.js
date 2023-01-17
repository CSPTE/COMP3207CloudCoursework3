import React, {useState} from 'react'
import "../styles/Signup.css"
import { Button, Form, Input, Typography } from 'antd';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import { useSignIn } from "react-auth-kit";

export default function Signup() {
	const [email, setEmail] = useState("")
	const [password, setPassword] = useState("")
	const [name, setName] = useState("")
	const navigate = useNavigate()
	const signIn = useSignIn();

	let submitLogIn = async (e) => {
		console.log("1")
		e.preventDefault()
		const resp = await axios.post("https://izifood.azurewebsites.net/api/registerUser?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: email, password: password, name: name })
		console.log(resp.data)
		if (resp.data.result == true) {
			signIn({
				token: resp.data.token,
				expiresIn: 3600,
				tokenType: "Bearer",
				authState: { email: email,password: password },
			});
			document.cookie = "tabKey=dashboard";
			console.log("2")
			// localStorage.setItem("email", email)
			console.log(document.cookie)
			navigate("/dashboard")
		} else{
			alert(resp.data.msg)
		}
	}

	return (
		<div>
			<div className="centered-box">
				<Form>
					<Typography.Title level={3}>Signup Page</Typography.Title>
					<Form.Item>
						<Input prefix={<UserOutlined />} placeholder="Username" onChange={(e) => setName(e.target.value)}/>
					</Form.Item>
					<Form.Item>
						<Input prefix={<UserOutlined />} placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
					</Form.Item>
					<Form.Item>
						<Input.Password prefix={<LockOutlined />} placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
					</Form.Item>

					<Form.Item>
						<Button type="primary" htmlType="submit" block onClick={(e) => submitLogIn(e)}>
							Sign Up
						</Button>
						Or <a href="/login">Login here!</a>
					</Form.Item>

				</Form>

			</div>
		</div>
	)
}
