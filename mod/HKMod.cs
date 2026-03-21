using Modding;
using UnityEngine;

namespace HKMod
{
    public class HKMod : Mod
    {
        public override string GetVersion() => "0.1";

        public override void Initialize()
        {
            Log("HKMod initialized!");
        }
    }
}