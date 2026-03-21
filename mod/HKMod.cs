using Modding;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using Newtonsoft.Json;

namespace HKMod
{
    public class HKMod : Mod
    {
        public override string GetVersion() => "0.1";

        private TcpListener? _server;
        private Thread? _serverThread;
        private TcpClient? _client;
        private int _frameCount = 0;

        public override void Initialize()
        {
            Log("HKMod initialized!");
            _serverThread = new Thread(StartServer);
            _serverThread.IsBackground = true;
            _serverThread.Start();

            ModHooks.HeroUpdateHook += OnHeroUpdate;
        }

        private void StartServer()
        {
            _server = new TcpListener(IPAddress.Loopback, 11000);
            _server.Start();
            Log("TCP server started on port 11000");

            while (true)
            {
                Log("Waiting for connection...");
                _client = _server.AcceptTcpClient();
                Log("Python EA connected!");
            }
        }

        private void OnHeroUpdate()
        {
            if (_client == null || !_client.Connected) return;

            var hero = HeroController.instance;
            if (hero == null) return;

            _frameCount++;
            if (_frameCount % 3 != 0) return;

            var rb = hero.GetComponent<Rigidbody2D>();

            var state = new
            {
                x = hero.transform.position.x,
                y = hero.transform.position.y,
                vx = rb.velocity.x,
                vy = rb.velocity.y,
                onGround = hero.cState.onGround,
                jumping = hero.cState.jumping,
                dashing = hero.cState.dashing,
                health = PlayerData.instance.health
            };

            try
            {
                string json = JsonConvert.SerializeObject(state) + "\n";
                byte[] data = Encoding.UTF8.GetBytes(json);
                _client.GetStream().Write(data, 0, data.Length);
            }
            catch
            {
                _client = null;
            }
        }
    }
}