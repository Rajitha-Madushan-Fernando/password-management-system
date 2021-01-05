<h1 class="code-line" data-line-start=0 data-line-end=1 ><a id="Passwordmanagementsystem_0"></a>Password-management-system</h1>
<p class="has-line-data" data-line-start="1" data-line-end="2">A PMS(Password Management System) is an API that helps individuals securely store and manage all of their login credentials. This api is used to create strong, unique, complex passwords for web applications.</p>
<h2 class="code-line" data-line-start=3 data-line-end=4 ><a id="Getting_Started_3"></a>Getting Started</h2>
<p class="has-line-data" data-line-start="4" data-line-end="5">These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.</p>
<h3 class="code-line" data-line-start=6 data-line-end=7 ><a id="Setup_the_environment_6"></a>Setup the environment</h3>
<hr>
<ul>
<li class="has-line-data" data-line-start="11" data-line-end="12">
<h5 class="code-line" data-line-start=11 data-line-end=12 ><a id="Check_python_version__python_version_11"></a>Check python version <code>$ python --version</code></h5>
</li>
<li class="has-line-data" data-line-start="12" data-line-end="13">
<h5 class="code-line" data-line-start=12 data-line-end=13 ><a id="Check_pip_version__pip_version_12"></a>Check pip version <code>$ pip --version</code></h5>
</li>
<li class="has-line-data" data-line-start="13" data-line-end="14">
<h5 class="code-line" data-line-start=13 data-line-end=14 ><a id="Clone_the_project__git_clone_httpsgithubcomRajithaMadushanFernandopasswordmanagementsystemgit_13"></a>Clone the project <code>$ git clone https://github.com/Rajitha-Madushan-Fernando/password-management-system.git</code></h5>
</li>
<li class="has-line-data" data-line-start="14" data-line-end="15">
<h5 class="code-line" data-line-start=14 data-line-end=15 ><a id="Install_python_virtual_environment_pip_install_pipenv_14"></a>Install python virtual environment <code>pip install pipenv</code></h5>
</li>
<li class="has-line-data" data-line-start="15" data-line-end="16">
<h5 class="code-line" data-line-start=15 data-line-end=16 ><a id="Activate_Python_environment_pipenv_shell_15"></a>Activate Python environment <code>pipenv shell</code></h5>
</li>
<li class="has-line-data" data-line-start="16" data-line-end="18">
<h5 class="code-line" data-line-start=16 data-line-end=17 ><a id="Install_required_packages__pip_install_r_requirementstxt_16"></a>Install required packages  <code>pip install -r requirements.txt</code></h5>
</li>
</ul>
<h3 class="code-line" data-line-start=18 data-line-end=19 ><a id="Now_you_ready_to_run_the_application_18"></a>Now you ready to run the application</h3>
<hr>
<p class="has-line-data" data-line-start="21" data-line-end="22">This  password management system contain two environment variables. Test and <a href="http://Development.To">Development.To</a> check main functionalities, We need to run the system under <strong>development</strong> environment and if we want to test the system we need to run the system under <strong>test</strong> environment.</p>
<h4 class="code-line" data-line-start=23 data-line-end=24 ><a id="Run_the_system_under_Test_environment__Run_the_unit_test_cases_23"></a>Run the system under Test environment | Run the unit test cases</h4>
<h5 class="code-line" data-line-start=24 data-line-end=25 ><a id="Windows_24"></a>Windows</h5>
<pre><code>$env:FLASK_ENV = test
python -m unittest
</code></pre>
<h5 class="code-line" data-line-start=27 data-line-end=28 ><a id="Linux_27"></a>Linux</h5>
<pre><code>export FLASK_ENV=test
python -m unittest
</code></pre>
<h4 class="code-line" data-line-start=31 data-line-end=32 ><a id="Run_the_system_under_Development_environment_31"></a>Run the system under Development environment</h4>
<h5 class="code-line" data-line-start=32 data-line-end=33 ><a id="Windows_32"></a>Windows</h5>
<pre><code>$env:FLASK_ENV = development
python -m unittest
</code></pre>
<h5 class="code-line" data-line-start=35 data-line-end=36 ><a id="Linux_35"></a>Linux</h5>
<pre><code>export FLASK_ENV=development
python -m unittest
</code></pre>
<h5 class="code-line" data-line-start=39 data-line-end=40 ><a id="Note__Depends_on_your_requirement_you_need_to_change_the_environment_Otherwise_system_will_generate_errors_Ex_If_you_want_to_use_the_system_and_check_the_functionalities_Then_you_cannot_use_Test_environment_You_need_to_change_it_to_Development_environment_39"></a>Note : Depends on your requirement you need to change the environment. Otherwise system will generate errors. Ex: If you want to use the system and check the functionalities, Then you cannot use Test environment. You need to change it to <strong>Development environment</strong>.</h5>
<hr>
<h3 class="code-line" data-line-start=41 data-line-end=42 ><a id="PMS_Functionalities_41"></a>PMS Functionalities</h3>
<p class="has-line-data" data-line-start="42" data-line-end="43">This system functions mainly devided to two categories. <strong>ADMIN</strong> and <strong>USER</strong>.  Some task can be perform by Admin only. In the first section list down all  function which required Admin access.</p>
<h3 class="code-line" data-line-start=43 data-line-end=44 ><a id="Admin__Tasks_43"></a>Admin  Tasks</h3>
<h5 class="code-line" data-line-start=44 data-line-end=45 ><a id="Login_to_system_using_master_password__Admin_44"></a>Login to system using master password - Admin</h5>
<p class="has-line-data" data-line-start="45" data-line-end="50"><code>http://127.0.0.1:5000/login</code><br>
<code>{ &quot;email&quot;: &quot;admin@admin.com&quot;, &quot;password&quot;: &quot;123DEs!678&quot; }</code></p>
<h5 class="code-line" data-line-start=51 data-line-end=52 ><a id="Note__After_having_the__successfully_loginThe_system_generate_a_Json_web_token_For_all_other_tasks_we_need_to_give_this_token_as_a_authentication_mechanisam_To_do_that_you_have_to_pass_the_token_in_the_postman_header_field_51"></a>Note : After having the  successfully login,The system generate a Json web token. For all other tasks we need to give this token as a authentication mechanisam. To do that you have to pass the token in the postman header field.</h5>
<p class="has-line-data" data-line-start="52" data-line-end="53"><code>x-access-tokens : &quot;your token goes here&quot;</code></p>
<h5 class="code-line" data-line-start=55 data-line-end=56 ><a id="Create_new_legacy_application__AdminToken_Required_55"></a>Create new legacy application - Admin[Token Required]</h5>
<p class="has-line-data" data-line-start="56" data-line-end="62"><code>http://127.0.0.1:5000/add_new_legacy_app</code><br>
<code>{ &quot;app_name&quot;:&quot;HRM&quot;, &quot;url&quot;:&quot;www.sample.com&quot;, &quot;description&quot;:&quot;Sample data&quot; }</code></p>
<h5 class="code-line" data-line-start=62 data-line-end=63 ><a id="View_all_registered_User_list__AdminToken_Required_62"></a>View all registered User list - Admin[Token Required]</h5>
<p class="has-line-data" data-line-start="63" data-line-end="64"><code>http://127.0.0.1:5000/all_users</code></p>
<hr>
<h3 class="code-line" data-line-start=69 data-line-end=70 ><a id="Normal_User_Tasks_69"></a>Normal User Tasks</h3>
<h5 class="code-line" data-line-start=70 data-line-end=71 ><a id="View_the_password_complexityToken_Not_Required_70"></a>View the password complexity[Token Not Required]</h5>
<p class="has-line-data" data-line-start="71" data-line-end="72"><code>http://127.0.0.1:5000/get_pwd_criteria</code></p>
<h5 class="code-line" data-line-start=73 data-line-end=74 ><a id="Signin__to_system_73"></a>Signin  to system</h5>
<p class="has-line-data" data-line-start="74" data-line-end="80"><code>http://127.0.0.1:5000/signup</code><br>
<code>{ &quot;username&quot;:&quot;sam&quot;, &quot;password&quot;:&quot;Ab@#123sJK7&quot;, &quot;email&quot;:&quot;sam@gmail.com&quot; }</code></p>
<h5 class="code-line" data-line-start=81 data-line-end=82 ><a id="View_System_Legacy_application_listToken_Required_81"></a>View System Legacy application list[Token Required]</h5>
<p class="has-line-data" data-line-start="82" data-line-end="83"><code>http://127.0.0.1:5000/app_list</code></p>
<h5 class="code-line" data-line-start=84 data-line-end=85 ><a id="Add_New_Legacy_app_Password_Token_Required__Main_task_of_the_PMS_84"></a>Add New Legacy app Password [Token Required] - Main task of the PMS</h5>
<p class="has-line-data" data-line-start="85" data-line-end="90"><code>http://127.0.0.1:5000/add_pwd</code><br>
<code>{ &quot;password&quot;:&quot;1@##D$D5fAcbA!&quot;, &quot;app_id&quot;:1, }</code></p>
<h5 class="code-line" data-line-start=91 data-line-end=92 ><a id="Get_all_passwords_for_current_logged_user_Token_Required_91"></a>Get all passwords for current logged user [Token Required]</h5>
<p class="has-line-data" data-line-start="92" data-line-end="93"><code>http://127.0.0.1:5000/pwd_list</code></p>
