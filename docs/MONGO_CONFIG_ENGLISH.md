# Database Configuration

## Create an account
1. Go to https://account.mongodb.com/account/login

2. Choose the authentication method and create the account (or log in if you already have one)

---

## Create an organization
> If you already have an organization created, skip this step

1. Go to https://cloud.mongodb.com/v2#/preferences/organizations

2. Click "**Create New Organization**"

![image](https://user-images.githubusercontent.com/63798776/188275387-9f80e7af-34f7-4984-9f2d-26d2665b81e7.png)

3. Enter the name of the organization and click "**Next**"

![image](https://user-images.githubusercontent.com/63798776/188275490-e11e424d-6fd5-47fc-a8f4-73706ec8ea08.png)

4. Click "**Create Organization**"

![image](https://user-images.githubusercontent.com/63798776/188275549-16236411-e936-4228-a11e-65285053257c.png)

---

## Create a project
1. Click "**New Project**"

![image](https://user-images.githubusercontent.com/63798776/188275607-3d013048-c8c9-4009-bd8a-f07dbb736aad.png)

2. Enter the project name and click "**Next**"

![image](https://user-images.githubusercontent.com/63798776/188275903-01b84d0b-6ea2-4133-92b0-36b05fe9104e.png)

3. Click "**Create Project**"

![image](https://user-images.githubusercontent.com/63798776/188275952-94cab590-8c34-40a5-853f-2037cad2c292.png)

---

## Create the database
1. Click "**Build a Database**"

![image](https://user-images.githubusercontent.com/63798776/188276061-ab428b17-fad2-41c7-bc3f-8c12a3ee0ef9.png)

2. Select the database type (_Shared_, as it is free).

![image](https://user-images.githubusercontent.com/63798776/171946060-a1c5b919-7ef4-44b7-b9e7-fdf51692867e.png)

3. Click **Create Cluster**.

4. Enter the database user name and password and click "**Create User**"

![image](https://user-images.githubusercontent.com/63798776/188276205-d6b42c03-d34d-449c-9fc2-de66e2167110.png)

5. Add the address `0.0.0.0/0` and click "**Add Entry**"

![image](https://user-images.githubusercontent.com/63798776/188276321-05819081-48af-44a7-b22c-5d1f7b5e52ed.png)

6. Click on "**Finish and Close**", then on "**Go to Database**" (in the _popup_ that appears)

7. Click **Connect**

![image](https://user-images.githubusercontent.com/63798776/171948956-e92e426d-6265-4987-89da-070cf5ecc43c.png)

8. Click **Connect your application**

![image](https://user-images.githubusercontent.com/63798776/188276469-a35b6ccb-b1a2-4d30-acdb-75066e3c2b16.png)

9. Select the Python _driver_ and copy the URL that will be generated

![image](https://user-images.githubusercontent.com/63798776/171949064-4b8f1a82-0b3c-4eb7-92e8-2f8d7964542a.png)


```env
# URL structure:
mongodb+srv://USERNAME:PASSWORD@CLUSTER.HASH.mongodb.net/DATABASE?retryWrites=true&w=majority
```

> NOTE: CLUSTER and HASH are defined by MongoDB, do not change them!

10. Replace **USERNAME** and **PASSWORD** with the data entered in point **4** of [database creation](#create-the-database).

11. Replace **DATABASE** with the name of the database (e.g. **pc2i-db**)

```env
# Example of a valid URL:
mongodb+srv://user-name:strong-password@cluster0.rxjhpdm.mongodb.net/pc2i-db?retryWrites=true&w=majority
```

## Now go back to [platform configuration](./README.md#6-create-the-environment-variables-file) and add the URL in the `.env` file